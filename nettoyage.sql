-- =====================================================================
--  MARDI  -  Â« Est-ce qu'on peut le faire en SQL ? Â»
--
--  Oui. Et de deux facons qui ne font pas du tout la meme chose.
--  Vous avez pose la question : voici la reponse complete.
-- =====================================================================

select c.segment_client  from clients c 
group by segment_client;
-- ---------------------------------------------------------------------
-- FACON 1 : NETTOYER A LA LECTURE  -  une VUE
--
-- Une vue est une requete a laquelle on donne un nom.
-- Elle ne stocke rien. Chaque fois qu'on l'interroge, elle recalcule.
-- La table d'origine n'est JAMAIS modifiee.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW v_reservations_propre AS
SELECT reservation_id, client_id, chambre_id,
       date_reservation, date_arrivee, date_depart, statut,
       CASE WHEN upper(trim(canal_reservation)) = 'TELEPHONE' THEN 'Téléphone'
            ELSE initcap(trim(canal_reservation))
       END AS canal_reservation,
       montant_total
FROM reservations;

--****************************************************************************************
--La question, et elle n’est pas technique : après la vue, qu’est-ce qui a
--été modifié dans la base ?
--*****************************************************************************************

-- ce qui a été modifié aprés la vue c'est que l'on a réussi à harmoniser le canal des reservations en particulier celles
-- effectuées au téléphone. En effet, téléphone était écrit de maniéres différentes.

-- On l'interroge comme une table :
SELECT canal_reservation, count(*) AS nb
FROM v_reservations_propre
GROUP BY canal_reservation ORDER BY nb DESC;
-- 4 lignes : Site Web 779, Booking 609, Agence 405, TÃ©lÃ©phone 207

-- Et la table d'origine n'a pas bouge :
SELECT count(DISTINCT canal_reservation) AS toujours_sale FROM reservations;
-- 8


-- ---------------------------------------------------------------------
-- FACON 2 : CORRIGER UNE FOIS POUR TOUTES  -  des UPDATE
--
-- On travaille sur une COPIE. On ne modifie jamais la table d'origine
-- tant qu'on n'est pas certain -- et on n'est jamais certain du premier coup.
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS reservations_copie;
CREATE TABLE reservations_copie AS SELECT * FROM reservations;

UPDATE reservations_copie SET canal_reservation = trim(canal_reservation);
-- PostgreSQL repond : UPDATE 2000
UPDATE reservations_copie SET canal_reservation = initcap(canal_reservation);
-- UPDATE 2000
UPDATE reservations_copie SET canal_reservation = 'Téléphone'
WHERE canal_reservation = 'Telephone';
-- UPDATE 9

SELECT canal_reservation, count(*) AS nb
FROM reservations_copie GROUP BY canal_reservation ORDER BY nb DESC;
-- 4 lignes, les memes qu'avec la vue

SELECT count(*) 
FROM reservations_copie 
WHERE canal_reservation <> trim(canal_reservation);

-- ---------------------------------------------------------------------
-- DEUX PIEGES, ET LES DEUX SONT SILENCIEUX
-- ---------------------------------------------------------------------

-- PIEGE 1 : Â« UPDATE 2000 Â» ne veut PAS dire que 2000 valeurs etaient fausses.
-- Il veut dire que PostgreSQL a reecrit 2000 lignes -- la plupart a l'identique.
-- Combien etaient REELLEMENT mal ecrites ? Il faut le demander :
SELECT count(*) AS vraiment_mal_ecrites
FROM reservations
WHERE canal_reservation NOT IN ('Site web', 'Booking', 'Agence', 'TÃ©lÃ©phone');
-- 30 lignes sur 2000.


-- ---------------------------------------------------------------------
-- PIEGE 2 : LE NETTOYAGE QUI ABIME PLUS QU'IL NE REPARE
--
-- initcap() met une majuscule a CHAQUE mot.
SELECT initcap('site web') AS resultat;
-- Â« Site Web Â», avec un W majuscule. Or le libelle officiel d'UrbanStay
-- est Â« Site web Â». On vient d'inventer une valeur qui n'existait nulle part.
--
-- Mesurons les degats :
SELECT count(*) FILTER (WHERE canal_reservation
                          NOT IN ('Site web','Booking','Agence','Téléphone'))  AS a_reparer,
       count(*) FILTER (WHERE canal_reservation
                          <> initcap(trim(canal_reservation)))                 AS modifiees_par_initcap,
       count(*) FILTER (WHERE canal_reservation
                              IN ('Site web','Booking','Agence','Téléphone')
                          AND canal_reservation
                          <> initcap(trim(canal_reservation)))                 AS correctes_abimees
FROM reservations;
-- a_reparer = 30   modifiees_par_initcap = 793   correctes_abimees = 772


-- les 30 à réparer car n'étant pas dans les canaux des reservations, ce filtre compte les reservations qui ne sont pas 
-- faites dans les canaux officiels, Cela permet de détecter les erreurs de saisie, les fautes d'orthographe
-- (ex: « Site webb », « Telefone »), ou les valeurs bizarres/inconnues qui traînent dans ta base et qu'il faut nettoyer.
-
-- Les 793 lignes ou les deux canaux sont différents, 
--
--  Cela permet de mesurer combien de lignes ont des problèmes de formatage de texte (par exemple : tout en majuscules 
-- comme "SITE WEB", tout en minuscules comme "booking", ou avec des espaces en trop comme " Agence " au lieu de "Agence").

-- 772 lignes justes detruites pour en reparer 30. Vingt-six fois plus de
-- degats que de reparations. ET AUCUN MESSAGE D'ERREUR.

-- 772 lignes ont des problèmes de formatage de texte (par exemple : tout en majuscules comme
--  "SITE WEB", tout en minuscules comme "booking", ou avec des espaces en trop comme " Agence " au lieu de "Agence").


-- ---------------------------------------------------------------------
-- LA VERSION QUI N'ABIME RIEN
--
-- On ne FABRIQUE pas le libelle avec une fonction : on le CHOISIT dans
-- une liste de valeurs officielles. La fonction sert seulement a
-- reconnaitre la ligne, jamais a produire le resultat.
-- ---------------------------------------------------------------------
SELECT CASE WHEN upper(trim(canal_reservation)) IN ('TELEPHONE','TÉLÉPHONE') THEN 'Téléphone'
            WHEN upper(trim(canal_reservation)) = 'SITE WEB'                 THEN 'Site web'
            WHEN upper(trim(canal_reservation)) = 'BOOKING'                  THEN 'Booking'
            WHEN upper(trim(canal_reservation)) = 'AGENCE'                   THEN 'Agence'
       END AS canal,
       count(*) AS nb
FROM reservations GROUP BY canal ORDER BY nb DESC;
-- Site web 779, Booking 609, Agence 405, TÃ©lÃ©phone 207.
-- Les quatre libelles officiels, et pas un de plus.
--
-- A RETENIR : une fonction de nettoyage sert a RECONNAITRE une valeur,
-- pas a la FABRIQUER. Des qu'on la laisse fabriquer, elle invente.