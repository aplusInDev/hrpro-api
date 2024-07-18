-- insert new evaluations

LOCK TABLES `evaluations` WRITE;

INSERT INTO `evaluations` (id, created_at, updated_at, employee_id, training_id, score, feedback, anonimous)
VALUES
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b1', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2111', 'training-9aff-400f-a21c-af244ced2111', 5, 'Great training!', 1),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b2', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2111', 'training-9aff-400f-a21c-af244ced2112', 4, 'Good training!', 0),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b3', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2111', 'training-9aff-400f-a21c-af244ced2113', 3, 'Average training!', 0),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b4', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2112', 'training-9aff-400f-a21c-af244ced2111', 2, 'Bad training!', 1),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b5', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2112', 'training-9aff-400f-a21c-af244ced2112', 1, 'Terrible training!', 0),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b6', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2112', 'training-9aff-400f-a21c-af244ced2113', 5, 'Great training!', 1),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b7', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2113', 'training-9aff-400f-a21c-af244ced2111', 4, 'Good training!', 1),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b8', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2113', 'training-9aff-400f-a21c-af244ced2112', 3, 'Average training!', 1),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b9', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2113', 'training-9aff-400f-a21c-af244ced2113', 2, 'Bad training!', 0),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1ba', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2114', 'training-9aff-400f-a21c-af244ced2111', 1, 'Terrible training!', 0),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1bb', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2114', 'training-9aff-400f-a21c-af244ced2112', 5, 'Great training!', 1),
  ('evalb1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1bc', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'cd736ecb-9aff-400f-a21c-af244ced2114', 'training-9aff-400f-a21c-af244ced2113', 4, 'Good training!', 1);

UNLOCK TABLES;
