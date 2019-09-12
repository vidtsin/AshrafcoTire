# -*- coding: utf-8 -*-
import sys
from datetime import datetime
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.isky_fingerprint_scheduler.zk import ZK, const


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    device_id = fields.Char(string='Biometric Device ID', help='Select the ZK device')


class ZkMachine(models.Model):
    _name = 'zk.machine'

    name = fields.Char(string='Machine IP', required=True, help='IP address of ZK Machine')
    port_no = fields.Integer(string='Port No', required=True, help='Port number of ZK Machine')
    address_id = fields.Many2one('res.partner', string='Working Address')
    machine_name = fields.Char(string='Machine Name')
    machine_sn = fields.Char(string='Machine SN ')
    machine_id = fields.Char(string='Machine ID ')
    machine_model = fields.Char(string='Machine Model')
    state = fields.Selection([('new', 'New'),('working', 'Working') ,('maintenance', 'Maintenance'),('broken', 'Broken')])
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    bu_id =fields.Many2one('account.analytic.tag', string='Project/BU')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = '[' + str(record.machine_name) + '] '+ str(record.name)
            result.append((record.id, name))
        return result

    @api.multi
    def device_connect(self, zk):
        try:
            conn = zk.connect()
        except:
            conn = False
        return conn

    @api.multi
    def clear_attendance(self):
        for device in self:
            machine_ip = device.name
            port = device.port_no
            zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, verbose=False)
            conn = zk.connect()
            conn.disable_device()
            conn.enable_device()
            if conn:
                try:
                    conn.clear_attendance()
                except:
                    raise UserError(_('Unable to clear attendance'))

            else:
                raise UserError(_('Unable to connect, please check the parameters and network connections. '))
            if conn:
                conn.disconnect()

    @api.multi
    def download_attendance(self):
        zk_attendance = self.env['zk.machine.attendance']
        for device in self:
            machine_ip = device.name
            port = device.port_no
            zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, verbose=False)
            print(zk,'cccc')
            conn = self.device_connect(zk)
            print(':::::::::::::::::::::::::::::::::::::::::conn',conn)
            if conn:
                try:
                    zk.enable_device()
                    attendance = conn.get_attendance()
                except:
                    attendance = False
                if attendance:
                    for each in attendance:
                        atten_time = each.timestamp
                        atten_time = datetime.strptime(
                            atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(
                            self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(atten_time, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        atten_time = datetime.strptime(
                            utc_dt, "%Y-%m-%d %H:%M:%S")
                        atten_time = fields.Datetime.to_string(atten_time)
                        get_user_id = self.env['hr.employee'].search(
                            [('device_id', '=', str(each.user_id))])
                        if get_user_id:
                            duplicate_atten_ids = zk_attendance.search(
                                [('device_id', '=', str(each.user_id)), ('punching_time', '=', atten_time)])
                            if duplicate_atten_ids:
                                continue
                            else:
                                zk_attendance.create({'employee_id': get_user_id.id,
                                                      'device_id': str(each.user_id),
                                                      'attendance_type': '1',
                                                      'punch_type': str(each.status),
                                                      'punching_time': atten_time,
                                                      'address_id': device.address_id.id,
                                                      'bu_id': device.bu_id.id})
                        else:
                            employee = self.env['hr.employee'].create(
                                {'device_id': str(each.user_id),'employee_variety': False ,'name': 'Fingerprint Employee/' + str(each.user_id)})
                            zk_attendance.create({'employee_id': employee.id,
                                                  'device_id': each.user_id,
                                                  'attendance_type': '1',
                                                  'punch_type': str(each.status),
                                                  'punching_time': atten_time,
                                                  'address_id': device.address_id.id,
                                                  'bu_id': device.bu_id.id})
                    return True
                else:
                    raise UserError(_('Unable to get the attendance log, please try again later.'))
            else:
                raise UserError(_('Unable to connect, please check the parameters and network connections.'))

    def _fetch_attendance(self):
        self.search([]).download_attendance()