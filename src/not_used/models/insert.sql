INSERT INTO "user" (username, mentor, email, password, name, surname, dob, tel, date_joined, photo, comfort_time, course, faculty, links, bio, xp, city, education, achievments) VALUES
('john_doe', FALSE, 'john.doe@example.com', 'securepassword123', 'John', 'Doe', '1995-04-23', '555-1234', CURRENT_TIMESTAMP, 'http://example.com/photos/johndoe', 'Evenings on weekdays', 'Engineering', 'Engineering and Technology', 'http://example.com/johndoe/socials', 'Just a regular guy who loves tech.', 1, 'spb', 'HSE', {'first': 0, 'second': 0, 'third': 0}),
('jane_doe', TRUE, 'jane.doe@example.com', 'janesecurepassword', 'Jane', 'Doe', '1993-08-15', '555-5678', CURRENT_TIMESTAMP, 'http://example.com/photos/janedoe', 'Weekends', 'Medicine', 'Health Sciences', 'http://example.com/janedoe/socials', 'Aspiring doctor and part-time mentor.', 10, 'spb', 'HSE', {'first': 1, 'second': 0, 'third': 0}),
('alex_smith', FALSE, 'alex.smith@example.com', 'alexspassword', 'Alex', 'Smith', '1989-12-10', '555-9012', CURRENT_TIMESTAMP, 'http://example.com/photos/alexsmith', 'Weekday mornings', 'Literature', 'Arts and Humanities', 'http://example.com/alexsmith/socials', 'Literature enthusiast and writer.', 111, 'spb', 'HSE', {'first': 1, 'second': 0, 'third': 0}),
('lisa_ray', TRUE, 'lisa.ray@example.com', 'lisarpassword', 'Lisa', 'Ray', '1997-05-22', '555-3456', CURRENT_TIMESTAMP, 'http://example.com/photos/lisaray', 'Afternoon to early evenings', 'Computer Science', 'Computer Science and Informatics', 'http://example.com/lisaray/socials', 'Coding wizard and tech mentor.', 11, 'spb', 'HSE', {'first': 0, 'second': 1, 'third': 1}),
('mike_jordan', FALSE, 'mike.jordan@example.com', 'mikejpassword', 'Mike', 'Jordan', '1991-02-14', '555-7890', CURRENT_TIMESTAMP, 'http://example.com/photos/mikejordan', 'Flexible', 'Business Administration', 'Business and Management', 'http://example.com/mikejordan/socials', 'Entrepreneur and business enthusiast.', 1000, 'msk', 'HSE', {'first': 1, 'second': 1, 'third': 1});

INSERT INTO club (owner, name, dest, photo, bio, links, date_created, date_joined, comfort_time) VALUES
(1, 'Tech Innovators', 'Technology and Innovation Hub', 'http://example.com/photos/techinnovators', 'A club for those passionate about technology and innovation.', 'http://example.com/techinnovators/socials', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Weekends'),
(2, 'Health Heroes', 'Community Health Initiatives', 'http://example.com/photos/healthheroes', 'Dedicated to improving community health through education and volunteering.', 'http://example.com/healthheroes/socials', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Weekday evenings'),
(3, 'Literary Legends', 'Book Clubs and Writing Workshops', 'http://example.com/photos/literarylegends', 'A sanctuary for those who find solace in words and narratives.', 'http://example.com/literarylegends/socials', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Wednesday nights'),
(4, 'Code Crafters', 'Coding Projects and Hackathons', 'http://example.com/photos/codecrafter', 'Bringing together coding enthusiasts to build and learn.', 'http://example.com/codecrafter/socials', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Saturdays'),
(5, 'Business Builders', 'Entrepreneurship and Networking Events', 'http://example.com/photos/businessbuilders', 'Fostering a community of aspiring entrepreneurs and business leaders.', 'http://example.com/businessbuilders/socials', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Monthly Fridays');

INSERT INTO club_x_user (club_id, user_id, role, date_joined) VALUES
(1, 1, 'Member', CURRENT_TIMESTAMP),
(2, 2, 'Owner', CURRENT_TIMESTAMP),
(3, 3, 'Member', CURRENT_TIMESTAMP),
(4, 4, 'Owner', CURRENT_TIMESTAMP),
(5, 5, 'Member', CURRENT_TIMESTAMP),
(1, 3, 'Member', CURRENT_TIMESTAMP),
(2, 4, 'Member', CURRENT_TIMESTAMP),
(3, 5, 'Member', CURRENT_TIMESTAMP),
(4, 1, 'Member', CURRENT_TIMESTAMP),
(5, 2, 'Owner', CURRENT_TIMESTAMP





delete from club_x_user;
delete from club;
delete from "user";