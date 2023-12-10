USE dice_and_die;
-- Create Ranks:
INSERT INTO ranks (name) VALUES ('stone');
INSERT INTO ranks (name) VALUES ('iron');
INSERT INTO ranks (name) VALUES ('bronze');
INSERT INTO ranks (name) VALUES ('silver');
INSERT INTO ranks (name) VALUES ('gold');
INSERT INTO ranks (name) VALUES ('platinum');
INSERT INTO ranks (name) VALUES ('diamond');

---- Create First Fake User
INSERT INTO users (email, password) VALUES ("fake_user@gmail.com", "FAKE_PASSWORD");
---- Get the ID of the last inserted user
SET @last_user_id = LAST_INSERT_ID();
INSERT INTO users_level (user_id, current_points, next_level_points) VALUES (@last_user_id, 0, 100);






