-- Dumping data for `accounts` table
USE hrpro_accounts_db;


LOCK TABLES `accounts` WRITE;


INSERT INTO accounts (id, email, hashed_password, employee_id, role, is_active)
VALUES
('account-8543-4342-8931-7fc7472f95ec', 'abdessamad.laabid@edu.uiz.ac.ma', '$2b$12$KnA2hO4wPI5flElmOEU5I.LIdkntprRVJarJpUQv9ccLLXrEzJhHO', 'admin-9aff-400f-a21c-af244ced2111', 'admin', 1);


UNLOCK TABLES;


-- Dumping data for `companies` table
USE hrpro_dev_db;


LOCK TABLES `companies` WRITE;


INSERT INTO `companies` (id, name, created_at, updated_at, address)
VALUES
('company-2d0a-4279-90ae-c6fe33172c0e', 'test company', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'AV 56 LOT DOUNIA 02 OULAD TEIMA');


UNLOCK TABLES;


-- Dumping data for `forms` table
LOCK TABLES `forms` WRITE;


INSERT INTO `forms` (id, created_at, updated_at, name, company_id)
VALUES
('form-8543-4342-8931-7fc7472f9510', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'employee', 'company-2d0a-4279-90ae-c6fe33172c0e'),
('form-8543-4342-8931-7fc7472f9511', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'job', 'company-2d0a-4279-90ae-c6fe33172c0e'),
('form-8543-4342-8931-7fc7472f9512', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'department', 'company-2d0a-4279-90ae-c6fe33172c0e');


UNLOCK TABLES;


-- Dumping data for `fields` table
LOCK TABLES `fields` WRITE;


INSERT INTO `fields` (id, created_at, updated_at, form_id, name, type)
VALUES
('field-8543-4342-8931-7fc7472f9510', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'form-8543-4342-8931-7fc7472f9510', 'first name', 'text'),
('field-8543-4342-8931-7fc7472f9511', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'form-8543-4342-8931-7fc7472f9510', 'last name', 'text'),
('field-8543-4342-8931-7fc7472f9512', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'form-8543-4342-8931-7fc7472f9510', 'email', 'email'),
('field-8543-4342-8931-7fc7472f9513', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'form-8543-4342-8931-7fc7472f9511', 'title', 'text'),
('field-8543-4342-8931-7fc7472f9514', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'form-8543-4342-8931-7fc7472f9512', 'name', 'text');


UNLOCK TABLES;


-- Dumping data for `employees` table
LOCK TABLES `jobs` WRITE;


INSERT INTO `jobs` (id, title, created_at, updated_at, company_id, info)
VALUES
('job-8543-4342-8931-7fc7472f9510', 'hr', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e', '{"title": "hr"}'),
('job-8543-4342-8931-7fc7472f9511', 'test job', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e', '{"title": "test job"}');


UNLOCK TABLES;


-- Dumping data for `departments` table
LOCK TABLES `departments` WRITE;


INSERT INTO `departments` (id, name, created_at, updated_at, company_id, info)
VALUES
('department-20ec-439f-9e10-bb6dfdb9ff10', 'hr', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e', '{"name": "hr"}'),
('department-20ec-439f-9e10-bb6dfdb9ff11', 'test department', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e', '{"name": "test department"}');


UNLOCK TABLES;


-- Dumping data for `employees` table
LOCK TABLES `employees` WRITE;


INSERT INTO `employees` (id, created_at, updated_at, first_name, last_name, company_id, job_id, department_id, info, hire_date)
VALUES
('admin-9aff-400f-a21c-af244ced2111', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "abdessamad", "plus", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9510', 'department-20ec-439f-9e10-bb6dfdb9ff10', '{"first_name": "abdessamad", "last_name": "plus", "email": "abdessamad.laabid@edu.uiz.ac.ma"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2111', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus1", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus1", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2112', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus2", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus2", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2113', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus3", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus3", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2114', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus4", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus4", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2115', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus5", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus5", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2116', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus6", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus6", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2117', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus7", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus7", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2118', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus8", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus8", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2119', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus9", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus9", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2120', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus10", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus10", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2121', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus11", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus11", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2122', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus12", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus12", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2123', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus13", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus13", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2124', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus14", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus14", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2125', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus15", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus15", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2126', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus16", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus16", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2127', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus17", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus17", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2128', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus18", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus18", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2129', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus19", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus19", "last_name": "test"}', '2024-05-13'),
('employee-9aff-400f-a21c-af244ced2130', '2024-05-13 18:38:28', '2024-05-13 18:38:28', "aplus20", "test", 'company-2d0a-4279-90ae-c6fe33172c0e', 'job-8543-4342-8931-7fc7472f9511', 'department-20ec-439f-9e10-bb6dfdb9ff11', '{"first_name": "aplus20", "last_name": "test"}', '2024-05-13');


UNLOCK TABLES;
