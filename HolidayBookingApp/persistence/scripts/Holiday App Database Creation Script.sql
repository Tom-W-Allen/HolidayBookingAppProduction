-- Script to be run by Python via Sqlite. Must be run within target database
DROP TABLE IF EXISTS employee_projects;
DROP TABLE IF EXISTS requests;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
	user_id INT PRIMARY KEY NOT NULL,
	user_name VARCHAR(256) NOT NULL,
	user_password VARCHAR(256) NOT NULL,
	password_change VARCHAR(256),
	user_role VARCHAR(256) NOT NULL,
	first_name VARCHAR(256) NOT NULL,
	surname VARCHAR(256) NOT NULL,
	manager VARCHAR(256),
	email_address VARCHAR(256),
	reset_identifier VARCHAR(256),
	holidays_remaining INT NOT NULL,
	password_attempts INT NOT NULL
);
                   
CREATE TABLE requests (
	request_id INT PRIMARY KEY NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	employee_id INT NOT NULL,
	approver_id INT NOT NULL,
	request_status VARCHAR(256) NOT NULL,
	total_holidays INT NOT NULL,

	FOREIGN KEY (employee_id) REFERENCES users (user_id),
	FOREIGN KEY (approver_id) REFERENCES users (user_id)
);
                   
CREATE TABLE projects (
	project_id INT PRIMARY KEY NOT NULL,
	project_name VARCHAR(256) NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	project_lead_id INT NOT NULL,

	FOREIGN KEY (project_lead_id) REFERENCES users(user_id)
);
                   
CREATE TABLE employee_projects (
	project_id INT NOT NULL,
	employee_id INT NOT NULL,
	join_date DATE NOT NULL,
	leave_date DATE NOT NULL,

    PRIMARY KEY (project_id, employee_id),
	FOREIGN KEY (project_id) REFERENCES projects (project_id),
	FOREIGN KEY (employee_id) REFERENCES users (user_id)
);