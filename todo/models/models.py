# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class TodoCategory(models.Model):
    _name = 'todo.category'
    _description = '分类'

    name = fields.Char('名称')
    task_ids = fields.One2many('todo.task', 'category_id', string='待办事项')
    count = fields.Integer('任务数量', compute='_compute_task_count')

    @api.depends('task_ids')
    @api.multi
    def _compute_task_count(self):
        for record in self:
            record.count = len(record.task_ids)


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = '待办事项'

    description = fields.Char('描述')
    is_done = fields.Boolean('已完成？')
    priority = fields.Selection([
        ('todo', '待办'),
        ('normal', '普通'),
        ('urgency', '紧急'),
    ], default='todo', string='紧急程度')
    deadline = fields.Datetime('截止时间')
    category_id = fields.Many2one('todo.category', string='分类')
    name = fields.Many2one('todo.user', string='用户名')
    language = fields.Char('语言')

    state = fields.Selection([
        ('draft', '草稿'),
        ('going', '进行中'),
        ('complete', '已完成'),
    ], string='状态', readonly=True, copy=False, default='draft', track_visibility='onchange')

    @api.model
    # def create(self, vals):
    #     print("hello", vals)
    #     names = vals['name']
    #     demo = self.env['todo_task'].search([('name', '=', 'names')])
    #     # if vals['name']:
    #     res = super(TodoTask, self).create(vals)
    #     return res

    @api.multi
    def button_draft(self):

        return self.write({'state': 'going'})

    @api.multi
    def button_going(self):
        return self.write({'state': 'complete'})

    @api.multi
    def button_complete(self):
        return self.write({'state': 'draft'})

    # @api.multi
    # def button_loading_draft(self):
    #     return self.write({'state': 'draft'})
    #
    # @api.multi
    # def button_done_draft(self):
    #     return self.write({'state': 'draft'})
    #
    @api.multi
    def button_audit(self):
        return {
            'name': '备注',
            'view_mode': 'form',
            'view_id': self.env.ref('todo.todo_user_view_form').id,
            'view_type': 'form',
            'res_model': 'todo.remark',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.onchange('name')
    def onchange_language(self):
        print(self.name)
        print(self.name.language)
        if self.name:
            self.language = self.name.language
        else:
            self.language = False

    button_status = fields.Boolean('提交状态', default=False, compute='button_status_judge')
    originator = fields.Many2one('res.users', string='发起人', default=lambda self: self.env.user)

    @api.one
    @api.depends('state')
    def button_status_judge(self):
        current_user_id = self.env.uid
        if self.state == 'draft' and current_user_id == self.originator.id:
            self.button_status = True
        else:
            self.button_status = False


class UserInfo(models.Model):
    _name = 'todo.user'
    _description = '用户信息'
    name = fields.Char('姓名')
    age = fields.Char('年龄')
    gender = fields.Char('性别')
    email_box = fields.Char('邮箱')
    language = fields.Char('语言')


class TodoRemarks(models.Model):
    _name = 'todo.remark'
    _description = '备注'
    name = fields.Char('姓名')
    age = fields.Char('年龄')
    gender = fields.Char('性别')
    education = fields.Selection([
        ('specialty', '专科'),
        ('undergraduate', '本科'),
        ('postgraduate', '研究生'),
    ], string='学历')
