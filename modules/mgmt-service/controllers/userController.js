const defineUserModel = require('../models/User');

exports.createUser = async (req, res) => {
  const User = await defineUserModel();
  const user = await User.create(req.body);
  res.status(201).send(user);
};

exports.getUsers = async (req, res) => {
  const User = await defineUserModel();
  const users = await User.findAll({ include: 'Role' });
  res.send(users);
};

exports.getUser = async (req, res) => {
  const User = await defineUserModel();
  const user = await User.findByPk(req.params.id, { include: 'Role' });
  res.send(user);
};

exports.updateUser = async (req, res) => {
  const User = await defineUserModel();
  const user = await User.findByPk(req.params.id);
  await user.update(req.body);
  res.send(user);
};

exports.deleteUser = async (req, res) => {
  const User = await defineUserModel();
  const user = await User.findByPk(req.params.id);
  await user.destroy();
  res.status(204).send();
};