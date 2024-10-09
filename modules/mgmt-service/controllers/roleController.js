const defineRoleModel = require('../models/Role');

exports.createRole = async (req, res) => {
  const Role = await defineRoleModel();
  const role = await Role.create(req.body);
  res.status(201).send(role);
};

exports.getRoles = async (req, res) => {
  const Role = await defineRoleModel();
  const roles = await Role.findAll();
  res.send(roles);
};

exports.getRole = async (req, res) => {
  const Role = await defineRoleModel();
  const role = await Role.findByPk(req.params.id);
  res.send(role);
};

exports.updateRole = async (req, res) => {
  const Role = await defineRoleModel();
  const role = await Role.findByPk(req.params.id);
  await role.update(req.body);
  res.send(role);
};

exports.deleteRole = async (req, res) => {
  const Role = await defineRoleModel();
  const role = await Role.findByPk(req.params.id);
  await role.destroy();
  res.status(204).send();
};