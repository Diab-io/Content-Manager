from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class ArticleController(http.Controller):

    #Helper methods
    def prepare_response(self, response, stat):
        if stat == 'error':
            response = str(response)
        data = {'status': stat, 'response': response}
        return data

    def is_date_format(self, date_string):
        date_format = '%d/%m/%Y'
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    #Api endpoint definitions
    @http.route('/api/content_manager/create', auth='none', type='json', methods=['POST'])
    def create_article(self, **kw):
        """ Api endpoint for the creation of articles """
        try:
            assigned_to = kw.get('assigned_to')
            publish_date = kw.get('publish_date')
            content = kw.get('content')
            title = kw.get('title')
            deadline = kw.get('deadline')
            response = []
            """ Checks for model sanity """
            if not assigned_to or publish_date or not content or not title or not deadline:
                response.append('"assigned_to" "publish_date" "content" "title" "deadline" are required')
                return self.prepare_response(response=response, stat='error')
            if not isinstance(assigned_to, int):
                response.append('Invalid type for assigned_to please provide an integer')
                return self.prepare_response(response=response, stat='error')
            if not self.is_date_format(publish_date) or not self.is_date_format(deadline):
                response.append('Date fields should be in this format %d/%m/%Y')
                return self.prepare_response(response=response, stat='error')
            kw['author'] = request.env.user.partner_id.id
            article_object = request.env['article.article']
            create_article = article_object.create(kw)
            response.append({'id': create_article.id})
            return self.prepare_response(response=response, stat='success')
        except Exception as e:
            return self.prepare_response(response=e, stat='error')
        
    
    @http.route('/api/content_manager/delete/<int:id>', auth='none', type='json', methods=['DELETE'])
    def delete_article(self, id):
        """ Endpoint for record deletion """
        try:
            response = []
            if not request.env.user.has_group('content_manager.group_article_manager'): # if reader deny access
                response.append('You dont have authoriztion to delete this record')
                return self.prepare_response(response=response, stat='error')
            id = int(id)
            rec = request.env['article.article'].sudo().search([('id', '=', id)])
            if not rec:
                response.append('This record does not exist')
                return self.prepare_response(response=response, stat='error')
            deleted_record = rec.unlink()
            if deleted_record:
                resp = {'deleted_id': deleted_record.id}
                response.append(resp)
                return self.prepare_response(response=response, stat='success')
            response.append('An error occured while deleting record')
            return self.prepare_response(response=response, stat='error')
        except Exception as e:
            return self.prepare_response(response=e, stat='error')

    @http.route('/api/content_manager/update/<int:id>', auth='none', type='json', methods=['POST'])
    def update_article(self, id, **kw):
        response = []
        try:
            id = int(id)
            if request.env.user.has_group('content_manager.group_article_reader'):
                user_id = request.env.user.partner_id.id
                user_data = request.env['article.article'].search([('assigned_to', '=', user_id)]).ids
                if id not in user_data:
                    response.append("You are not authorised to update data or record does not exist")
                    return self.prepare_response(response=response, stat='error')
                elif len(kw.values()) > 1 or not kw.get('state'):
                    response.append("You can only update the state as an article reader")
                    return self.prepare_response(response=response, stat='error')

            # check Assigned_to is of type int
            if kw.get('assigned_to') and not isinstance(kw.get('assigned_to'), int):
                response.append('Please provide an integer for assigned_to')
                return self.prepare_response(response=response, stat='error')
            
            # Prevents author from being updated
            if kw.get('author'):
                response.append("Forbidden, you can't update the author of an article")
                return self.prepare_response(response=response, stat='error')

            rec_exists = request.env['article.article'].search([('id', '=', id)])
            if not rec_exists:
                response.append("Record does not exist")
                return self.prepare_response(response=response, stat='error')

            write_article = rec_exists.write(kw)
            vals = {'write_id': write_article.id}
            response.append(vals)
            return self.prepare_response(response=response, stat='success')           
        except Exception as e:
            return self.prepare_response(response=e, stat='error')

    @http.route('/web/session/authenticate', type='json', auth='none')
    def authenticate(self, **kw):
        _logger.info(f'------------- {kw}')
        request.session.authenticate(request.session.db, 'odimayodavid7@gmail.com', 'odimdavid2003')
        return request.env['ir.http'].session_info()

    @http.route('/api/content_manager/retrieve', auth='none', type='http', methods=['GET'])
    def fetch_record(self, **kw):
        """ Endpoint to fetch whole data or user specific data """
        try:
            if request.env.user.has_group('content_manager.group_article_manager'):
                articles = request.env['article.article'].sudo().search([])

            elif request.env.user.has_group('content_manager.group_article_reader'):
                user_id = request.env.user.partner_id.id
                articles = request.env['article.article'].search([('assigned_to', '=', user_id)])

            response = []
            for rec in articles:
                vals ={
                'id': rec.id,
                'title': rec.title, 
                'author': rec.author.name,
                'assigned_to': rec.assigned_to.name,
                'deadline': rec.deadline,
                'publish_date': rec.publish_date,
                'start_date': rec.start_date,
                'finished_date': rec.finished_date,
                'state': rec.state,
                'content': rec.content,
                'image': rec.image
                }
                response.append(vals)
            return self.prepare_response(response=response, stat='success')
        except Exception as e:
            return self.prepare_response(response=e, stat='error')
    