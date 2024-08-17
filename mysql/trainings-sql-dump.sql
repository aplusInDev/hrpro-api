-- Dumping data for `trainings` table
USE hrpro_dev_db;


LOCK TABLES `trainings` WRITE;


INSERT INTO `trainings` (id, created_at, updated_at, title, start_date, end_date, company_id)
VALUES
  ('training-9aff-400f-a21c-af244ced2111', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'training 1', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e'),
  ('training-9aff-400f-a21c-af244ced2112', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'training 2', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e'),
  ('training-9aff-400f-a21c-af244ced2113', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'training 3', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e'),
  ('training-9aff-400f-a21c-af244ced2114', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'training 4', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e'),
  ('training-9aff-400f-a21c-af244ced2115', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'training 5', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e'),
  ('training-9aff-400f-a21c-af244ced2116', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'training 6', '2024-05-13 18:38:28', '2024-05-13 18:38:28', 'company-2d0a-4279-90ae-c6fe33172c0e');


UNLOCK TABLES;