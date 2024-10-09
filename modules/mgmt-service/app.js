const express = require('express');
const bodyParser = require('body-parser');
const initializeDatabase = require('./config/database');
const consul = require('./config/consul'); // 导入 Consul 客户端

const userRoutes = require('./routes/userRoutes');
const roleRoutes = require('./routes/roleRoutes');
const botRoutes = require('./routes/botRoutes');

const app = express();

app.use(bodyParser.json());

app.use('/users', userRoutes);
app.use('/roles', roleRoutes);
app.use('/bots', botRoutes);

app.get('/health', (req, res) => {
  res.status(200).send('OK');
});


const serviceId = 'mgmt-service-1';
const serviceName = 'mgmt-service';
const serviceAddress = 'mgmt-service';
const servicePort = 3000;

consul.agent.service.register({
  id: serviceId,
  name: serviceName,
  address: serviceAddress,
  port: servicePort,
  check: {
    http: `http://${serviceAddress}:${servicePort}/health`,
    interval: '10s'
  }
}, (err) => {
  if (err) {
    console.error('Failed to register service to Consul:', err);
  } else {
    console.log('Service registered to Consul successfully');
  }
});

initializeDatabase().then(sequelize => {
  const server = app.listen(servicePort, async () => {
    await sequelize.sync();
    console.log(`Service running on port ${servicePort}`);
  });


  const deregisterService = () => {
    consul.agent.service.deregister(serviceId, (err) => {
      if (err) {
        console.error('Failed to deregister service from Consul:', err);
      } else {
        console.log('Service deregistered from Consul successfully');
      }
      process.exit();
    });
  };


  process.on('SIGINT', deregisterService);
  process.on('SIGTERM', deregisterService);
}).catch(err => {
  console.error('Failed to initialize database:', err);
});