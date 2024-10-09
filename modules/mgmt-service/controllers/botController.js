const defineBotModel = require('../models/Bot');

exports.createBot = async (req, res) => {
  const Bot = await defineBotModel();
  const bot = await Bot.create(req.body);
  res.status(201).send(bot);
};

exports.getBots = async (req, res) => {
  const Bot = await defineBotModel();
  const bots = await Bot.findAll({ include: 'User' });
  res.send(bots);
};

exports.getBot = async (req, res) => {
  const Bot = await defineBotModel();
  const bot = await Bot.findByPk(req.params.id, { include: 'User' });
  res.send(bot);
};

exports.updateBot = async (req, res) => {
  const Bot = await defineBotModel();
  const bot = await Bot.findByPk(req.params.id);
  await bot.update(req.body);
  res.send(bot);
};

exports.deleteBot = async (req, res) => {
  const Bot = await defineBotModel();
  const bot = await Bot.findByPk(req.params.id);
  await bot.destroy();
  res.status(204).send();
};