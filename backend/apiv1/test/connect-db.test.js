const connectDB = require('../../utils/connect-db');

jest.mock('mongodb', () => {
  return {
    MongoClient: jest.fn().mockImplementation(() => {
      return {
        connect: jest.fn(),
        close: jest.fn(),
      };
    }),
  };
});

test('connects to MongoDB', async () => {
  await connectDB();
  // Assertions to verify the mock was called
});