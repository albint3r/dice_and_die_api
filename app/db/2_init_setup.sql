USE dice_and_die;
-- Create Ranks:
INSERT INTO ranks (name) VALUES ('stone');
INSERT INTO ranks (name) VALUES ('iron');
INSERT INTO ranks (name) VALUES ('bronze');
INSERT INTO ranks (name) VALUES ('silver');
INSERT INTO ranks (name) VALUES ('gold');
INSERT INTO ranks (name) VALUES ('platinum');
INSERT INTO ranks (name) VALUES ('diamond');


INSERT INTO users (user_id,email, password, name, last_name) VALUES ("I007","fake_user1@gmail.com", "FAKE_PASSWORD", "John", "Doe");
INSERT INTO users_levels (user_id, exp_points, next_level_points) VALUES ("I007", 0, 50);
INSERT INTO bank_accounts (user_id) VALUES ("I007");

INSERT INTO users (user_id,email, password, name, last_name) VALUES ("I008","fake_user2@gmail.com", "FAKE_PASSWORD", "Jane", "Doe");
INSERT INTO users_levels (user_id, exp_points, next_level_points) VALUES ("I008", 0, 50);
INSERT INTO bank_accounts (user_id) VALUES ("I008");

INSERT INTO users (user_id,email, password, name, last_name) VALUES ("I009","fake_user3@gmail.com", "FAKE_PASSWORD", "Baby", "Babe");
INSERT INTO users_levels (user_id, exp_points, next_level_points) VALUES ("I009", 0, 50);
INSERT INTO bank_accounts (user_id) VALUES ("I009");

INSERT INTO users (user_id, email, password, name, last_name) VALUES
    ("FAKE001", "fake_user1@outlook.com", "FAKE_PASSWORD", "John", "Smith"),
    ("FAKE002", "fake_user2@outlook.com", "FAKE_PASSWORD", "Jane", "Doe"),
    ("FAKE003", "fake_user3@outlook.com", "FAKE_PASSWORD", "Michael", "Gonzalez"),
    ("FAKE004", "fake_user4@outlook.com", "FAKE_PASSWORD", "Samantha", "Martinez"),
    ("FAKE005", "fake_user5@outlook.com", "FAKE_PASSWORD", "David", "Rodriguez"),
    ("FAKE006", "fake_user6@outlook.com", "FAKE_PASSWORD", "Sarah", "Lopez"),
    ("FAKE007", "fake_user7@outlook.com", "FAKE_PASSWORD", "William", "Perez"),
    ("FAKE008", "fake_user8@outlook.com", "FAKE_PASSWORD", "Jessica", "Sanchez"),
    ("FAKE009", "fake_user9@outlook.com", "FAKE_PASSWORD", "James", "Ramirez"),
    ("FAKE010", "fake_user10@outlook.com", "FAKE_PASSWORD", "Ashley", "Torres"),
    ("FAKE011", "fake_user11@outlook.com", "FAKE_PASSWORD", "Christopher", "Flores"),
    ("FAKE012", "fake_user12@outlook.com", "FAKE_PASSWORD", "Amanda", "Gomez"),
    ("FAKE013", "fake_user13@outlook.com", "FAKE_PASSWORD", "Matthew", "Hernandez"),
    ("FAKE014", "fake_user14@outlook.com", "FAKE_PASSWORD", "Emily", "Diaz"),
    ("FAKE015", "fake_user15@outlook.com", "FAKE_PASSWORD", "Daniel", "Rivera"),
    ("FAKE016", "fake_user16@outlook.com", "FAKE_PASSWORD", "Ashley", "Cruz"),
    ("FAKE017", "fake_user17@outlook.com", "FAKE_PASSWORD", "Joshua", "Reyes"),
    ("FAKE018", "fake_user18@outlook.com", "FAKE_PASSWORD", "Jennifer", "Morales"),
    ("FAKE019", "fake_user19@outlook.com", "FAKE_PASSWORD", "Andrew", "Ortiz"),
    ("FAKE020", "fake_user20@outlook.com", "FAKE_PASSWORD", "Maria", "Gutierrez"),
    ("FAKE021", "fake_user21@outlook.com", "FAKE_PASSWORD", "Ryan", "Moreno"),
    ("FAKE022", "fake_user22@outlook.com", "FAKE_PASSWORD", "Nicole", "Castillo"),
    ("FAKE023", "fake_user23@outlook.com", "FAKE_PASSWORD", "Kevin", "Guerrero"),
    ("FAKE024", "fake_user24@outlook.com", "FAKE_PASSWORD", "Rachel", "Navarro"),
    ("FAKE025", "fake_user25@outlook.com", "FAKE_PASSWORD", "Brandon", "Vasquez"),
    ("FAKE026", "fake_user26@outlook.com", "FAKE_PASSWORD", "Rebecca", "Santos"),
    ("FAKE027", "fake_user27@outlook.com", "FAKE_PASSWORD", "Jacob", "Chavez"),
    ("FAKE028", "fake_user28@outlook.com", "FAKE_PASSWORD", "Megan", "Mendoza"),
    ("FAKE029", "fake_user29@outlook.com", "FAKE_PASSWORD", "Justin", "Silva"),
    ("FAKE030", "fake_user30@outlook.com", "FAKE_PASSWORD", "Vanessa", "Jimenez");

-- Estableciendo niveles y cuentas bancarias con variaciones del 1 al 15
INSERT INTO users_levels (user_id, exp_points, next_level_points, level)
VALUES
    ("FAKE001", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE002", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE003", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE004", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE005", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE006", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE007", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE008", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE009", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE010", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE011", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE012", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE013", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE014", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE015", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE016", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE017", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE018", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE019", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE020", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE021", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE022", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE023", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE024", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE025", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE026", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE027", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE028", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE029", 0, 50, FLOOR(1 + RAND() * 15)),
    ("FAKE030", 0, 50, FLOOR(1 + RAND() * 15));

INSERT INTO bank_accounts (user_id)
VALUES
    ("FAKE001"),
    ("FAKE002"),
    ("FAKE003"),
    ("FAKE004"),
    ("FAKE005"),
    ("FAKE006"),
    ("FAKE007"),
    ("FAKE008"),
    ("FAKE009"),
    ("FAKE010"),
    ("FAKE011"),
    ("FAKE012"),
    ("FAKE013"),
    ("FAKE014"),
    ("FAKE015"),
    ("FAKE016"),
    ("FAKE017"),
    ("FAKE018"),
    ("FAKE019"),
    ("FAKE020"),
    ("FAKE021"),
    ("FAKE022"),
    ("FAKE023"),
    ("FAKE024"),
    ("FAKE025"),
    ("FAKE026"),
    ("FAKE027"),
    ("FAKE028"),
    ("FAKE029"),
    ("FAKE030");

UPDATE users_levels
SET rank_id = (SELECT rank_id FROM ranks WHERE name = 'stone')
WHERE level < 5;

UPDATE users_levels
SET rank_id = (SELECT rank_id FROM ranks WHERE name = 'iron')
WHERE level >= 5 AND level < 10;

UPDATE users_levels
SET rank_id = (SELECT rank_id FROM ranks WHERE name = 'bronze')
WHERE level >= 10 AND level < 20;








