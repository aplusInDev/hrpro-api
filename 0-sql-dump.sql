-- adding new employees

LOCK TABLES `jobs` WRITE;

INSERT INTO `jobs` (id, title, created_at, updated_at, company_id, info)
VALUES ('9606262a-8543-4342-8931-7fc7472f95ec', 'test job', '2024-05-13 18:38:28', '2024-05-13 18:38:28', '34b36936-da9e-415d-9740-1a016eeccb19', '{"title": "test job"}');

UNLOCK TABLES;

LOCK TABLES `departments` WRITE;

INSERT INTO `departments` (id, name, created_at, updated_at, company_id, info)
VALUES ('3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', 'test department', '2024-05-13 18:38:28', '2024-05-13 18:38:28', '34b36936-da9e-415d-9740-1a016eeccb19', '{"name": "test department"}');

UNLOCK TABLES;

LOCK TABLES `employees` WRITE;

INSERT INTO `employees` (id, created_at, updated_at, first_name, last_name, company_id, job_id, department_id, info, position_info, hire_date)
VALUES ('cd736ecb-9aff-400f-a21c-af244ced2111', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus1", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus1", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2112', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus2", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus2", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2113', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus3", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus3", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2114', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus4", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus4", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2115', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus5", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus5", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2116', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus6", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus6", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2117', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus7", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus7", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2118', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus8", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus8", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2119', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus9", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus9", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2120', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus10", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus10", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2121', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus11", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus11", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2122', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus12", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus12", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2123', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus13", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus13", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2124', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus14", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus14", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2125', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus15", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus15", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2126', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus16", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus16", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2127', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus17", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus17", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2128', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus18", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus18", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2129', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus19", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus19", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13'),
('cd736ecb-9aff-400f-a21c-af244ced2130', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus20", "test", '34b36936-da9e-415d-9740-1a016eeccb19', '9606262a-8543-4342-8931-7fc7472f95ec', '3efd7921-20ec-439f-9e10-bb6dfdb9ffb1', '{"first name": "aplus20", "last name": "test"}', '{"department": "test department", "job_title": "test job"}', '2024-05-13');

UNLOCK TABLES;