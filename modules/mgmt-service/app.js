const express = require('express');
const app = express();

app.get('/health', (req, res) => {
  res.status(200).send('OK');  // Health check should return 200 OK
});

app.listen(3000, () => {
  console.log('Service running on port 3000');
});