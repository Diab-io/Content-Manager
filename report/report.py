# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class articleManagerReport(models.AbstractModel):
    _name = 'report.content_manager.report_article'
    _description = 'Content Manager Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'article.article'
        docs = self.env[model].browse(self.env.context.get('active_ids', docids))

        # filter out only report with read state
        docs = docs.filtered(lambda r: r.state == 'read')
        if not docs:
            raise ValidationError(_('Report(s) not in read state.'))

        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
        }