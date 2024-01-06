from odoo import models, fields, api

# class ChatgptWizard(models.TransientModel):
#     _name = 'chatgpt.wizard'
#     _description = 'wizard for communication'
#
#     name = fields.Char(string='Name')
#     output = fields.Char(string='Output', readonly=True)
#
#
#     def perform_action(self):
#         wizard=self
#         wizard.output = "Hello, " + wizard.name
#         self = self.with_context({'keep_open': True})
#         return {
#             'name': 'Medical Chatbot',
#             'type': 'ir.actions.act_window',
#             'res_model': self._name,
#             'res_id': self.id,
#             'view_mode': 'form',
#             'view_id': self.env.ref('medical_coding.chatgpt_wizard_view_form').id,
#             'target': 'new',
#         }
#
#     def clear_fields(self):
#         self.write({
#             'name': False,
#             'output': False,
#         })
#         self = self.with_context({'keep_open': True})
#         return {
#             'name': 'Medical Chatbot',
#             'type': 'ir.actions.act_window',
#             'res_model': self._name,
#             'res_id': self.id,
#             'view_mode': 'form',
#             'view_id': self.env.ref('medical_coding.chatgpt_wizard_view_form').id,
#             'target': 'new',
#         }


class ChatgptWizard(models.TransientModel):
    _name = 'chatgpt.wizard'
    _description = 'wizard for communication'

    name = fields.Char(string='Question')
    output = fields.Char(string='Output', readonly=True)

    def perform_action(self):
        def medchat(msg):
            import openai

            openai.api_key = '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'
            messages = [
                {"role": "system", "content": "You are a kind helpful assistant for madical coding."},
            ]

            while True:
                # message = input("User : ")
                message = msg
                if message:
                    messages.append(
                        {"role": "user", "content": message},
                    )
                    chat = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages=messages , max_tokens=40
                    )

                reply = chat.choices[0].message.content
                # print(f"ChatGPT: {reply}")
                messages.append({"role": "assistant", "content": reply})
                return reply


        wizard = self
        qst = 'provide ICD-10-CM medical code of ' + wizard.name + ' put the medical code and disease in separate double quotes in a max of 20 words'
        wizard.output = medchat(qst)

        # wizard.output = "check your keyword"





        import re

        try:

            value = re.findall(r'"(.*?)"', wizard.output)

            values = {
                "medical_code": value[0],
                "code_desc": value[1]
            }
            self.env['chatgpt.model'].create(values)

        except:
            wizard.output='some exception occured'

        #
        # codes=quoted_words[0]
        # des=quoted_words[1]

        # wizard.output = "Hello, " + wizard.name
        self = self.with_context({'keep_open': True})



        # main_model = self.env['chatgpt.model']
        # main_model.create({'medical_code': codes, 'code_desc': des})

        return {
            'name': 'Medical Chatbot',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('medical_coding.chatgpt_wizard_view_form').id,
            'target': 'new',
        }

    def clear_fields(self):
        self.write({
            'name': False,
            'output': False,
        })
        self = self.with_context({'keep_open': True})
        return {
            'name': 'Medical Chatbot',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('medical_coding.chatgpt_wizard_view_form').id,
            'target': 'new',
        }
    # model_name='chatgpt.wizard'
    #
    # env = api.Environment(models.SUPERUSER_ID, {})
    # your_model = env[model_name]
    #
    # # Fetch all records
    # records = your_model.search([])
    #
    # # Print values of 'name' and 'value' fields for each record
    # for record in records:
    #     print(f"Name: {record.name}, Value: {record.value}")



