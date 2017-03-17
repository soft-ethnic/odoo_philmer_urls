# -*- encoding: utf-8 -*-
import time
from openerp import tools
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import logging
from datetime import timedelta
from openerp.fields import Datetime as fdatetime
from calendar import monthrange
import calendar

_logger = logging.getLogger(__name__)

def number_of_days_in_next_months(start_date,number_of_months):
    year = int(start_date.strftime('%Y'))
    month = int(start_date.strftime('%m'))
    index = number_of_months
    days = 0
    while index > 0:
        days += calendar.monthrange(year,month)[1]
        month += 1
        if month > 12:
            month = 1
            year += 1
        index -= 1
    return days
def number_of_days_in_next_years(start_date,number_of_years):
    year = int(start_date.strftime('%Y'))
    month = int(start_date.strftime('%Y'))
    if month > 2: # if february is already past in the start date, we take first the following year into account; else this year and next years
        year += 1
    days = 0
    index = number_of_years
    while index > 0:
        days += calendar.isleap(year) and 366 or 365
        index -= 1
        year += 1
    return days

class philmer_url(models.Model):
    _name = 'philmer.url'
    _description = 'URL of website, blogs, web tools, web apps'
    _order = 'name'
    
    name = fields.Char('Name', required=True)
    url = fields.Char('URL', required=True)
    url_type = fields.Selection([('api','API'),('blog','Blog'),('forum','Forum'),('ftp','FTP'),('site','Site'),('shop','Shop'),('web_tool','Tool'),('web_app','Web App')],'Type')
    last_visit = fields.Datetime('Last Visit')
    type_freq = fields.Selection([('hour','Hour(s)'),('day','Day(s)'),('week','Week(s)'),('month','Month(s)'),('year','Year(s)'),('none','Never')],string='Frequency Type',default='none')
    duration_freq = fields.Integer('Duration',default=1,min=0)
    next_visit = fields.Datetime(string='Next Planned Visit',compute='_compute_next_visit',store=True,compute_sudo=False)
    comment = fields.Text('Comment')
    language_id = fields.Many2one('res.lang',string='Language')
    last_verification = fields.Date('Last Verification')
    wrong_verification = fields.Integer('Wrong last verifications')
    tag_ids = fields.Many2many('philmer.url.tag', relation='philmer_urls_tags', column1='url_id', column2='tag_id', string='Tags')
    user_id = fields.Many2one('res.users',string='User')
    confidential = fields.Boolean('Confidential',default=False)
    active = fields.Boolean('Active',default=True)
    
    @api.depends('last_visit','type_freq','duration_freq')
    def _compute_next_visit(self):
        for url in self.filtered('last_visit'):
            if url.type_freq != 'none':
                dLast = fdatetime.from_string(url.last_visit)
                if url.type_freq == 'hour':
                    dNext = dLast + timedelta(hours=(url.duration_freq or 0))
                elif url.type_freq == 'day':
                    dNext = dLast + timedelta(days=(url.duration_freq or 0))
                elif url.type_freq == 'week':
                    dNext = dLast + timedelta(days=((url.duration_freq or 0)*7))
                elif url.type_freq == 'month':
                    dNext = dLast + timedelta(days=number_of_days_in_next_months(dLast,url.duration_freq) )
                elif url.type_freq == 'year':
                    dNext = dLast + timedelta(days=number_of_days_in_next_years(dLast,url.duration_freq))
                else:
                    dNext = dLast
                url.next_visit = fdatetime.to_string(dNext)
            else:
                url.next_visit = False
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
