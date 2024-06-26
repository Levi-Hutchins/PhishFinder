const request = require("supertest");
const app = require("../../app");
jest.useFakeTimers();


describe("Test Email Service Functionality", () => {
  it("tests bad auth /api/email/get_email_data", async () => {
    const response = await request(app).get("/api/email/get_email_data");
    expect(response.statusCode).toBe(401);
  });
});