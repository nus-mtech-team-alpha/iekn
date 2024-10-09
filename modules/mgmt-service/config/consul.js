const Consul = require('consul');

const consul = new Consul({
  host: 'consul', // Consul 服务器的主机名
  port: 8500        // Consul 服务器的端口
});

module.exports = consul;