INSERT INTO users VALUES
(1, 'JNic87', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'basic', 'Jim', 'Nicholson', 4, NULL, NULL, 20, 0),
(2, 'Dev2024', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'basic', 'Sally', 'Smith', NULL, NULL, 4, 25, 0),
(3, 'Doug_42', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'basic', 'Doug', 'Fletcher', NULL, NULL, 4, 19, 0),
(4, 'TStev65', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'manager', 'Tim', 'Stevens', NULL, NULL, 0, 0, 0),
(5, 'MW_Dev', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'basic', 'Mark', 'White', 7, NULL, NULL, 23, 0),
(6, 'K_Dev', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'basic', 'Katie', 'Watts', 7, NULL, NULL, 16, 0),
(7, 'Sarah_B', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'manager', 'Sarah', 'Black', NULL, NULL, 0, 0, 0),
(8, 'Smithy_97', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'basic', 'Joe', 'Smith', 9, NULL, NULL, 25, 0),
(9, 'AlexC_2', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'manager', 'Alex', 'Cameron', NULL, NULL, 0, 0, 0),
(10, 'AStone_82', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', NULL, 'admin', 'Ashley', 'Stone', NULL, NULL, 0, 0, 0);

INSERT INTO requests VALUES
(1, '2024-3-4', '2024-3-8', 1, 4, 'approved', 5),
(2, '2024-4-22', '2024-4-24', 8, 9, 'pending', 3),
(3, '2023-11-6', '2023-11-6', 6, 7, 'approved', 1),
(4, '2024-7-29', '2024-8-9', 2, 4, 'cancelled', 10),
(5, '2024-9-23', '2024-10-2', 6, 7, 'approved', 8),
(6, '2024-4-15', '2024-4-16', 5, 7, 'approved', 2),
(7, '2024-11-18', '2024-11-25', 3, 4, 'approved', 6),
(8, '2024-3-4', '2024-3-9', 3, 4, 'rejected', 6),
(9, '2024-9-24', '2024-9-25', 5, 7, 'rejected', 2),
(10, '2024-2-1', '2024-11-25', 8, 9, 'cancelled', 1);

INSERT INTO projects VALUES
(1, 'Database Migration', '2024-7-1', '2024-12-31', 4),
(2, '.Net Upgrade', '2024-5-20', '2024-6-9', 4),
(3, 'E-Commerce API', '2025-1-1', '2025-12-31', 7),
(4, 'Data Analytics Dashboard', '2025-3-1', '2026-2-28', 4),
(5, 'Security Upgrade', '2024-10-14', '2025-2-1', 9),
(6, 'Internal API', '2026-1-1', '2026-3-31', 7),
(7, 'Firewall Upgrade', '2026-5-1', '2026-7-31', 9),
(8, 'NoSql Database Creation', '2027-1-1', '2027-6-30', 4),
(9, 'Protocol Update', '2027-2-1', '2027-3-31', 9),
(10, 'Python Upgrade', '2027-7-1', '2027-12-31', 4);

INSERT INTO employee_projects VALUES
(1, 1, '2024-7-1', '2024-12-31'),
(1, 2, '2024-7-1', '2024-12-31'),
(2, 2, '2024-5-20', '2024-6-9'),
(2, 3, '2024-5-20', '2024-6-9'),
(5, 8, '2024-10-14', '2025-2-1'),
(7, 8, '2026-5-1', '2026-7-31'),
(8, 1, '2027-1-1', '2027-6-30'),
(8, 2, '2027-1-1', '2027-6-30'),
(8, 3, '2027-1-1', '2027-6-30'),
(10, 1, '2027-7-1', '2027-12-31');