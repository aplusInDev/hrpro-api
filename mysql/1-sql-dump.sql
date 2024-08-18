-- Dumping data for `accounts` table
-- USE hrpro_accounts_db;


LOCK TABLES `accounts` WRITE;


INSERT INTO accounts (id, email, hashed_password, company_id, employee_id, role, is_active)
VALUES
('account-8543-4342-8931-7fc7472f95ec', 'laabid.abdessamadplus@gmail.com', '$2b$12$KnA2hO4wPI5flElmOEU5I.LIdkntprRVJarJpUQv9ccLLXrEzJhHO', 'company-2d0a-4279-90ae-c6fe33172c0e', 'admin-9aff-400f-a21c-af244ced2111', 'admin', 1);


UNLOCK TABLES;
