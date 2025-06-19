-- Parent categories
INSERT INTO categories (id, created_at, updated_at, deleted_at, name, type, user_id, parent_id) VALUES
-- EXPENSE
('a0cbd69e-381f-4e44-b0c3-c543d8e8e5c1', now(), now(), NULL, 'Housing', 'EXPENSE', '11e7437a-871d-410c-9266-5ed6bddf6fb1', NULL),
-- INCOME
('ce8a62ea-72f0-4cd3-8e6b-40434b313f23', now(), now(), NULL, 'Salary', 'INCOME', '11e7437a-871d-410c-9266-5ed6bddf6fb1', NULL),
-- ASSET
('cf0a49bd-4b7f-4602-9172-2539dbaf5b98', now(), now(), NULL, 'Bank Account', 'ASSET', '11e7437a-871d-410c-9266-5ed6bddf6fb1', NULL),
-- LIABILITY
('edb87945-fc4f-48fd-a458-34b4d25317f1', now(), now(), NULL, 'Credit Cards', 'LIABILITY', '11e7437a-871d-410c-9266-5ed6bddf6fb1', NULL),
-- EQUITY
('b1c8b560-d4b0-4e86-8be8-61f15cf3b1a1', now(), now(), NULL, 'Investments', 'EQUITY', '11e7437a-871d-410c-9266-5ed6bddf6fb1', NULL);

-- Subcategories
INSERT INTO categories (id, created_at, updated_at, deleted_at, name, type, user_id, parent_id) VALUES
-- EXPENSE subcategories
('91e4c91c-8598-4c4e-993b-3a7e7dd197ff', now(), now(), NULL, 'Rent', 'EXPENSE', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'a0cbd69e-381f-4e44-b0c3-c543d8e8e5c1'),
('3026883f-83dc-4895-bacc-d45e6b05d2d6', now(), now(), NULL, 'Utilities', 'EXPENSE', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'a0cbd69e-381f-4e44-b0c3-c543d8e8e5c1'),

-- INCOME subcategories
('8aa32f4b-55e1-4bc9-bf06-82db309271b1', now(), now(), NULL, 'Monthly Paycheck', 'INCOME', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'ce8a62ea-72f0-4cd3-8e6b-40434b313f23'),
('0197f520-31e9-4bd9-a29f-93cbde98d3c1', now(), now(), NULL, 'Bonus', 'INCOME', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'ce8a62ea-72f0-4cd3-8e6b-40434b313f23'),

-- ASSET subcategories
('c3992637-7836-49b7-9440-b8abdb27284f', now(), now(), NULL, 'Checking Account', 'ASSET', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'cf0a49bd-4b7f-4602-9172-2539dbaf5b98'),
('7f2f763f-7c60-4f94-92fa-3128c7cf0a79', now(), now(), NULL, 'Savings Account', 'ASSET', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'cf0a49bd-4b7f-4602-9172-2539dbaf5b98'),

-- LIABILITY subcategories
('e9f21e20-8b5a-4d3d-a0ec-e13edda045b6', now(), now(), NULL, 'Visa Card', 'LIABILITY', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'edb87945-fc4f-48fd-a458-34b4d25317f1'),
('ff1e601a-1055-4e2d-91d2-f9aa5565b2c3', now(), now(), NULL, 'MasterCard', 'LIABILITY', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'edb87945-fc4f-48fd-a458-34b4d25317f1'),

-- EQUITY subcategories
('b6f1fa2a-e3a5-420e-9f0d-7d6df9f1c758', now(), now(), NULL, 'Stocks', 'EQUITY', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'b1c8b560-d4b0-4e86-8be8-61f15cf3b1a1'),
('5ff3e52f-0d2d-4c59-9e0e-131dd3a3b2c4', now(), now(), NULL, 'Retirement Fund', 'EQUITY', '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'b1c8b560-d4b0-4e86-8be8-61f15cf3b1a1');

-- Transactions
INSERT INTO transactions (id, created_at, updated_at, deleted_at, amount, description, category_id, date, user_id) VALUES
('a1f7b4e9-1d36-4e8b-b8a2-3bc67a55e7c1', now(), now(), NULL, 1200, 'Monthly Rent Payment', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff', '2025-06-01', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('1c9f9638-8500-4207-a285-870ff68f9fbc', now(), now(), NULL, 85, 'Hydro Bill', '3026883f-83dc-4895-bacc-d45e6b05d2d6', '2025-06-05', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('c7f1c1b3-cf1e-4f34-a4b7-145b71202f62', now(), now(), NULL, 3000, 'May Salary', '8aa32f4b-55e1-4bc9-bf06-82db309271b1', '2025-05-30', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('f4f95bc2-d3aa-47a9-b04d-65fd59c35b55', now(), now(), NULL, 500, 'Performance Bonus', '0197f520-31e9-4bd9-a29f-93cbde98d3c1', '2025-05-15', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('f93deff9-c97f-4e4f-aed9-02a3556f9b25', now(), now(), NULL, 450, 'Groceries', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff', '2025-06-08', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('d28728f3-7897-49cf-9c66-52ec87f7f81c', now(), now(), NULL, 100, 'Checking Deposit', 'c3992637-7836-49b7-9440-b8abdb27284f', '2025-06-01', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('eff6d7d2-d7c5-4b88-94d6-607ec2c65c52', now(), now(), NULL, 150, 'Credit Card Interest', 'e9f21e20-8b5a-4d3d-a0ec-e13edda045b6', '2025-06-03', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('f6d74a47-7a96-4766-9d5f-fc6bc9cc3445', now(), now(), NULL, 200, 'Visa Bill Payment', 'e9f21e20-8b5a-4d3d-a0ec-e13edda045b6', '2025-06-04', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('ae4c73e5-fd00-48e0-b74f-f78d3a96e199', now(), now(), NULL, 500, 'Buy TSLA stock', 'b6f1fa2a-e3a5-420e-9f0d-7d6df9f1c758', '2025-05-25', '11e7437a-871d-410c-9266-5ed6bddf6fb1'),
('6a5b6d4d-f97f-4bfc-b703-1b5fce7372ed', now(), now(), NULL, 1000, 'Transfer to Retirement Fund', '5ff3e52f-0d2d-4c59-9e0e-131dd3a3b2c4', '2025-06-06', '11e7437a-871d-410c-9266-5ed6bddf6fb1');

--Budget
INSERT INTO budgets (id, created_at, updated_at, deleted_at, user_id, name, description, amount, type, frequency, start_date, end_date) VALUES
('1bdba4a7-2752-4f1d-b15a-70b1b346fbaf', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Monthly Rent Budget', 'Cap rent at $1300/month', 1300, 'FIXED', 'MONTHLY', '2025-06-01', NULL),
('78d15ce4-e0c7-4564-85be-018015c1099c', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Utility Budget', 'Electric, water, etc.', 200, 'FLEXIBLE', 'MONTHLY', '2025-06-01', NULL),
('f5c91e3c-96ea-41f5-a9ae-5c1ae28aa02f', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Grocery Budget', 'Food and home supplies', 600, 'FLEXIBLE', 'MONTHLY', '2025-06-01', NULL),
('ad7fbd0c-195f-46e7-b7bb-9ffb9d50806a', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Credit Card Budget', 'Visa and Mastercard payments', 800, 'FIXED', 'MONTHLY', '2025-06-01', NULL),
('6d77f625-845e-446e-a319-2e6a9829e3b9', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Savings Budget', 'Transfer to savings', 1000, 'ROLLING', 'MONTHLY', '2025-06-01', NULL),
('2cc0a38d-6d53-48ed-98e5-646b91a9b0db', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Investment Budget', 'Monthly investment in stocks', 500, 'FIXED', 'MONTHLY', '2025-06-01', NULL),
('41dc07fb-b5f5-4db7-829f-6d3be997b084', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Retirement Budget', '401K and TFSA contributions', 1000, 'ROLLING', 'MONTHLY', '2025-06-01', NULL),
('ec29d59e-b14f-44f5-b94d-7995c6ae7756', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Vacation Budget', 'Save for annual trip', 3000, 'SAVINGS', 'YEARLY', '2025-01-01', '2025-12-31'),
('0e8b160f-e3e2-4c4e-bd74-7c11035e0a4e', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Emergency Fund', 'Backup savings', 5000, 'SAVINGS', 'YEARLY', '2025-01-01', NULL),
('be17f18f-6a3d-4dd9-9e6e-f0331f4a1ef6', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Dining Budget', 'Dining out limit', 200, 'FLEXIBLE', 'MONTHLY', '2025-06-01', NULL);

--Categories-Budgets
INSERT INTO categories_budgets (budget_id, category_id) VALUES
('1bdba4a7-2752-4f1d-b15a-70b1b346fbaf', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff'),
('78d15ce4-e0c7-4564-85be-018015c1099c', '3026883f-83dc-4895-bacc-d45e6b05d2d6'),
('f5c91e3c-96ea-41f5-a9ae-5c1ae28aa02f', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff'),
('ad7fbd0c-195f-46e7-b7bb-9ffb9d50806a', 'e9f21e20-8b5a-4d3d-a0ec-e13edda045b6'),
('6d77f625-845e-446e-a319-2e6a9829e3b9', '7f2f763f-7c60-4f94-92fa-3128c7cf0a79'),
('2cc0a38d-6d53-48ed-98e5-646b91a9b0db', 'b6f1fa2a-e3a5-420e-9f0d-7d6df9f1c758'),
('41dc07fb-b5f5-4db7-829f-6d3be997b084', '5ff3e52f-0d2d-4c59-9e0e-131dd3a3b2c4'),
('ec29d59e-b14f-44f5-b94d-7995c6ae7756', '7f2f763f-7c60-4f94-92fa-3128c7cf0a79'),
('0e8b160f-e3e2-4c4e-bd74-7c11035e0a4e', 'c3992637-7836-49b7-9440-b8abdb27284f'),
('be17f18f-6a3d-4dd9-9e6e-f0331f4a1ef6', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff');

--Goals
INSERT INTO goals (id, created_at, updated_at, deleted_at, user_id, name, description, target, start_date, end_date, status) VALUES
('f80bc011-0a9d-429a-87f3-8765bb6c7f5a', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Vacation to Japan', 'Save for Japan trip', 3000, '2025-01-01', '2025-12-01', 'IN_PROGRESS'),
('f2a233b9-91fa-4f49-b6a2-6a457b8f344e', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Emergency Fund', 'Emergency savings goal', 5000, '2025-01-01', '2025-12-31', 'IN_PROGRESS'),
('b3d3ed4f-cd50-470c-918e-26162c512a20', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'New Laptop', 'MacBook Pro upgrade', 2000, '2025-06-01', '2025-10-01', 'IN_PROGRESS'),
('7c107558-0e91-4f2b-94b0-49c7e3dfbbf6', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Wedding Fund', 'Save for wedding expenses', 15000, '2025-01-01', '2026-06-01', 'IN_PROGRESS'),
('5be7d031-507e-4ee3-8d56-afe61844de3d', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Home Downpayment', 'Future home', 50000, '2025-01-01', '2028-01-01', 'IN_PROGRESS'),
('baf9d6be-1a38-4bc5-bab3-04f4f7995d30', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Birthday Gift', 'Gift for partner', 300, '2025-08-01', '2025-10-01', 'IN_PROGRESS'),
('a73d7ae7-bf4b-4d91-b218-8415e60704b8', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Camera Upgrade', 'Sony A7 IV', 2500, '2025-05-01', '2025-12-01', 'IN_PROGRESS'),
('268f6a60-1a8c-4d91-9e91-c7ff02a3a3e4', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Tuition Fee', 'Graduate school savings', 15000, '2025-01-01', '2026-01-01', 'IN_PROGRESS'),
('ae61bcb2-17f8-4d80-8d8f-9e72dbeb4056', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Pet Emergency Fund', 'Vet expenses', 800, '2025-03-01', '2025-12-01', 'IN_PROGRESS'),
('663d22ee-bb60-4f84-b878-149f1c34e187', now(), now(), NULL, '11e7437a-871d-410c-9266-5ed6bddf6fb1', 'Car Maintenance', 'Yearly upkeep', 1500, '2025-01-01', '2025-12-31', 'IN_PROGRESS');

--Categories-Goals
INSERT INTO categories_goals (goal_id, category_id) VALUES
('f80bc011-0a9d-429a-87f3-8765bb6c7f5a', '7f2f763f-7c60-4f94-92fa-3128c7cf0a79'),
('f2a233b9-91fa-4f49-b6a2-6a457b8f344e', 'c3992637-7836-49b7-9440-b8abdb27284f'),
('b3d3ed4f-cd50-470c-918e-26162c512a20', 'c3992637-7836-49b7-9440-b8abdb27284f'),
('7c107558-0e91-4f2b-94b0-49c7e3dfbbf6', '7f2f763f-7c60-4f94-92fa-3128c7cf0a79'),
('5be7d031-507e-4ee3-8d56-afe61844de3d', '7f2f763f-7c60-4f94-92fa-3128c7cf0a79'),
('baf9d6be-1a38-4bc5-bab3-04f4f7995d30', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff'),
('a73d7ae7-bf4b-4d91-b218-8415e60704b8', 'b6f1fa2a-e3a5-420e-9f0d-7d6df9f1c758'),
('268f6a60-1a8c-4d91-9e91-c7ff02a3a3e4', 'c3992637-7836-49b7-9440-b8abdb27284f'),
('ae61bcb2-17f8-4d80-8d8f-9e72dbeb4056', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff'),
('663d22ee-bb60-4f84-b878-149f1c34e187', '91e4c91c-8598-4c4e-993b-3a7e7dd197ff');
