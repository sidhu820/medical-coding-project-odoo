from odoo import models, fields, api

class ChatgptModel(models.Model):
    _name = 'chatgpt.model'
    _description = 'chatbot for medical coding...'

    medical_code = fields.Char(string='code')
    code_desc=fields.Char(string="description")

    def open_wizard(self):
        return {
            'name': 'Medical Chatbot',
            'type': 'ir.actions.act_window',
            'res_model': 'chatgpt.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('medical_coding.chatgpt_wizard_view_form').id,
            'target': 'new',
        }
