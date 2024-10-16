const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    viewportWidth: 1920, // đặt chiều rộng cho toàn màn hình
    viewportHeight: 1080, // đặt chiều cao cho toàn màn hình
    specPattern: 'cypress/e2e/*.cy.js', // Chạy tất cả file .cy.js
  },
});
