-- Seed a starter universe so company search works before external APIs
INSERT INTO investory.companies (ticker, name, exchange)
VALUES
    ('AAPL', 'Apple Inc.', 'NASDAQ'),
    ('MSFT', 'Microsoft Corporation', 'NASDAQ'),
    ('GOOGL', 'Alphabet Inc. Class A', 'NASDAQ'),
    ('AMZN', 'Amazon.com Inc.', 'NASDAQ'),
    ('META', 'Meta Platforms Inc.', 'NASDAQ'),
    ('NVDA', 'NVIDIA Corporation', 'NASDAQ'),
    ('TSLA', 'Tesla Inc.', 'NASDAQ'),
    ('JPM', 'JPMorgan Chase & Co.', 'NYSE'),
    ('V', 'Visa Inc.', 'NYSE'),
    ('WMT', 'Walmart Inc.', 'NYSE'),
    ('JNJ', 'Johnson & Johnson', 'NYSE'),
    ('XOM', 'Exxon Mobil Corporation', 'NYSE')
ON CONFLICT (ticker) DO NOTHING;
