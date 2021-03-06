from db_init import db
from utils import to_json
from rep.models_beehive import Experiment

import datetime
import json
import uuid, collections


class CalendarConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    event_num_limit = db.Column(db.String(5))
    event_time_limit = db.Column(db.String(10))
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))

    def __init__(self, info):
        self.event_num_limit = info.get('event_num_limit')
        self.event_time_limit = info.get('event_time_limit')
        self.code = info.get('code')

    def __repr__(self):
        result = {'id': self.id,
                  'event_time_limit': self.event_time_limit,
                  'event_num_limit': self.event_num_limit,
                  'code': self.code,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        if not info.get('event_num_limit') and not info.get('event_time_limit'):
            print '**********************'
            print 'calendar params: {}'.format(info)
            print '**********************'
            return (-1, 'No calendar params', -1)

        existing_experiment = Experiment.query.filter_by(code=info['code']).first()
        if not existing_experiment:
            invalid_response = 'Invalid experiment code({})'.format(info['code'])
            return (-1, invalid_response, -1)

        new_setting = CalendarConfig(info)
        db.session.add(new_setting)
        db.session.commit()

        return (200, 'Successfully added cal setting.', new_setting)


class DailyReminderConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    reminder_time = db.Column(db.String(10))

    def __init__(self, info):
        self.reminder_time = info.get('reminder_time')
        self.code = info.get('code')

    def __repr__(self):
        result = {'id': self.id,
                  'reminder_time': self.reminder_time,
                  'code': self.code,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        if not info.get('reminder_time'):
            return (-1, 'No reminder_time params', -1)

        existing_experiment = Experiment.query.filter_by(code=info['code']).first()
        if not existing_experiment:
            invalid_response = 'Invalid experiment code({})'.format(info['code'])
            return (-1, invalid_response, -1)

        new_reminder = DailyReminderConfig(info)
        db.session.add(new_reminder)
        db.session.commit()
        return (200, 'Successfully added daily reminder.', new_reminder)


class GeneralNotificationConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))
    intv_id = db.relationship('Intervention', backref='general_notification_config', lazy='select')

    title = db.Column(db.String(50))
    content = db.Column(db.String(50))
    app_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.title = info.get('title')
        self.content = info.get('content')
        self.app_id = info.get('app_id')
        self.code = info.get('code')

    def __repr__(self):
        result = {'id': self.id,
                  'title': self.title,
                  'content': self.content,
                  'app_id': self.app_id,
                  'code': self.code,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        existing_experiment = Experiment.query.filter_by(code=info['code']).first()
        if not existing_experiment:
            invalid_response = 'Invalid experiment code({})'.format(info['code'])
            return (-1, invalid_response, -1)

        new_notif = GeneralNotificationConfig(info)
        db.session.add(new_notif)
        db.session.commit()
        return (200, 'Successfully added general notification setting.', new_notif)


class ImageTextUpload(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(100))
    image_name = db.Column(db.String(100))
    text = db.Column(db.String(1500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))

    def __init__(self, info):
        self.image_url = info['image_url']
        self.image_name = info['image_name']
        self.text = info['text']
        self.code = info['code']

    def __repr__(self):
        result = {'id': self.id,
                  'image_url': self.image_url,
                  'image_name': self.image_name,
                  'text': self.text,
                  'code': self.code,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        if ImageTextUpload.query.filter_by(image_url=info['image_url'], text=info['text']).first():
            return

        new_image = ImageTextUpload(info)
        db.session.add(new_image)
        db.session.commit()


class Intervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notif_id = db.Column(db.Integer, db.ForeignKey('general_notification_config.id'))
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    treatment = db.Column(db.String(2000))
    start = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    every = db.Column(db.String(30))
    when = db.Column(db.String(30))
    repeat = db.Column(db.String(30))
    intv_type = db.Column(db.String(20))
    user_window_hours = db.Column(db.Integer)
    free_hours_before_sleep = db.Column(db.Integer)

    def __init__(self, info):
        self.code = info['code']
        self.treatment = info['treatment']
        self.start = info['start']
        self.end = info['end']
        self.every = info['every']
        self.when = info['when']
        self.repeat = info['repeat']
        self.intv_type = info['intv_type']
        self.notif_id = info['notif_id']
        self.user_window_hours = info['user_window_hours']
        self.free_hours_before_sleep = info['free_hours_before_sleep']

    def __repr__(self):
        treatment_image = []
        treatment_text = []
        if self.treatment:
            json_treatment = json.loads(self.treatment)
            for treat_id in json_treatment.values():
                txt_img = ImageTextUpload.query.get(treat_id)
                treatment_image.append(txt_img.image_url)
                treatment_text.append(txt_img.text)

        notif = GeneralNotificationConfig.query.filter_by(id=self.notif_id).first()
        if not notif:
            notif = '{}'
        else:
            notif = json.dumps({'title': notif.title, 'content': notif.content, 'app_id': notif.app_id})
        result = {
            'created_at': str(self.created_at),
            'code': self.code,
            'treatment_image': treatment_image,
            'treatment_text': treatment_text,
            'start': str(self.start),
            'end': str(self.end),
            'every': self.every,
            'when': self.when,
            'repeat': self.repeat,
            'user_window_hours': self.user_window_hours,
            'free_hours_before_sleep': self.free_hours_before_sleep,
            'notif_id': self.notif_id,
            'notif': notif,
            'intv_type': self.intv_type
        }
        return json.dumps(result)

    @staticmethod
    def add_intervention(info):
        new_intervention = Intervention(info)
        db.session.add(new_intervention)
        db.session.commit()
        latest_intervention = Intervention.query.order_by('created_at desc').first()
        return (200, 'Successfully added intervention', latest_intervention)

    @staticmethod
    def delete_intervention(created_at):
        Intervention.query.filter_by(created_at=created_at).delete()
        db.session.commit()


class Mturk(db.Model):
    worker_id = db.Column(db.String(120), primary_key=True, unique=True)
    moves_id = db.Column(db.String(120), unique=True)
    access_token = db.Column(db.String(120), unique=True)
    refresh_token = db.Column(db.String(120), unique=True)
    code = db.Column(db.String(120), unique=True)
    ip = db.Column(db.String(24))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.code = Mturk.generate_unique_id()

    def __repr__(self):
        return 'worker_id: {}/moves_id: {}'.format(self.worker_id, self.moves_id)

    @staticmethod
    def generate_unique_id():
        code = str(uuid.uuid4())[:6]
        while Mturk.query.filter_by(code=code).first():
            code = str(uuid.uuid4())[:6]
        return code

    @staticmethod
    def get_worker(worker_id):
        """
        Return user object from database using primary_key(email).
        """
        return Mturk.query.get(worker_id)

    @staticmethod
    def add_user(info):
        """ add new mturk user and return worker generated code if adding new worker """
        existing_worker = Mturk.query.filter_by(worker_id=info['worker_id']).first()
        existing_moves = Mturk.query.filter_by(moves_id=info['moves_id']).first()

        if existing_moves:
            return (-1, 'Moves app has already been connected. Contact Mturk requester.', existing_worker.code)
        elif existing_worker:
            return (-1, 'Worker has already been verified. Contact Mturk requester.', existing_worker.code)

        worker = Mturk(info['worker_id'])
        worker.moves_id = info['moves_id']
        worker.access_token = info['access_token']
        worker.refresh_token = info['refresh_token']
        worker.code = str(uuid.uuid4())
        worker.ip = str(info['ip'])

        db.session.add(worker)
        db.session.commit()

        return (200, 'Successfully connected your moves app!', worker.code)

    def update_field(self, key, value):
        """
        Set user field with give value and save to database.
        """
        worker = Mturk.query.get(self.worker_id)
        setattr(worker, key, value)
        db.session.commit()


class MturkPrelimRecruit(db.Model):
    worker_id = db.Column(db.String(50), primary_key=True)
    worker_code = db.Column(db.String(10), unique=True)
    device_id = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.worker_id = info['worker_id']
        self.worker_code = MturkPrelimRecruit.generate_unique_id()
        self.device_id = info['device_id']

    @staticmethod
    def generate_unique_id():
        code = str(uuid.uuid4())[:6]
        while MturkPrelimRecruit.query.filter_by(worker_code=code).first():
            code = str(uuid.uuid4())[:6]
        return code

    def __repr__(self):
        result = {'device_id': self.device_id,
                  'worker_id': self.worker_id,
                  'worker_code': self.worker_code,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add_worker(info):
        enrolled_worker = MturkPrelimRecruit.query.filter_by(worker_id=info['worker_id']).first()
        enrolled_device = MturkPrelimRecruit.query.filter_by(device_id=info['device_id']).first()
        if enrolled_worker:
            return (200, 'Worker already added.', enrolled_worker)
        elif enrolled_device:
            return (-1, 'Device already registered.', enrolled_worker)

        new_worker = MturkPrelimRecruit(info)
        db.session.add(new_worker)
        db.session.commit()

        return (200, 'Successfully submitted worker id.', new_worker)


class MturkExclusive(db.Model):
    worker_id = db.Column(db.String(50), primary_key=True)
    worker_code = db.Column(db.String(10), unique=True)
    experiment_group = db.Column(db.String(10))
    experiment_code = db.Column(db.String(50))
    experiment_label = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.worker_id = info['worker_id']
        self.worker_code = MturkExclusive.generate_unique_id()
        self.experiment_group = info['experiment_group']
        self.experiment_code = info['experiment_code']
        self.experiment_label = info['experiment_label']

    @staticmethod
    def generate_unique_id():
        code = str(uuid.uuid4())[:6]
        while MturkExclusive.query.filter_by(worker_code=code).first():
            code = str(uuid.uuid4())[:6]
        return code

    def __repr__(self):
        result = {
            'worker_id': self.worker_id,
            'worker_code': self.worker_code,
            'experiment_group': self.experiment_group,
            'experiment_code': self.experiment_code,
            'experiment_label': self.experiment_label,
            'created_at': str(self.created_at)
        }
        return json.dumps(result)

    @staticmethod
    def add(info):
        enrolled_worker = MturkExclusive.query.filter_by(
            worker_id=info['worker_id'], experiment_code=info['experiment_code']).first()
        if enrolled_worker:
            return (-1, 'Worker already enrolled in experiment.', enrolled_worker)

        new_worker = MturkExclusive(info)
        db.session.add(new_worker)
        db.session.commit()

        return (200, 'Successfully enrolled worker_id in experiment', new_worker)


class MturkFBStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.String(50))
    device_id = db.Column(db.String(30))
    total_seconds = db.Column(db.Integer)
    total_opens = db.Column(db.Integer)
    time_spent = db.Column(db.Integer)
    time_open = db.Column(db.Integer)
    ringer_mode = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # additional params (added: March 10)
    current_fb_max_time = db.Column(db.Integer, default=-1)
    current_fb_max_opens = db.Column(db.Integer, default=-1)
    current_treatment_start_date = db.Column(db.DateTime)
    current_followup_start_date = db.Column(db.DateTime)
    current_logging_stop_date = db.Column(db.DateTime)

    def __init__(self, info):
        self.worker_id = info['worker_id']
        self.device_id = info['device_id']
        self.total_seconds = info['total_seconds']
        self.total_opens = info['total_opens']
        self.time_spent = info['time_spent']
        self.time_open = info['time_open']
        self.ringer_mode = info['ringer_mode']

        self.current_fb_max_time = info.get('current_fb_max_time')
        self.current_fb_max_opens = info.get('current_fb_max_opens')
        self.current_treatment_start_date = info.get('current_treatment_start_date')
        self.current_followup_start_date = info.get('current_followup_start_date')
        self.current_logging_stop_date = info.get('current_logging_stop_date')

    def __repr__(self):
        result = {
            'worker_id': self.worker_id,
            'device_id': self.device_id,
            'total_seconds': self.total_seconds,
            'total_opens': self.total_opens,
            'time_spent': self.time_spent,
            'time_open': self.time_open,
            'ringer_mode': self.ringer_mode,
            'created_at': str(self.created_at),
            'current_fb_max_time': self.current_fb_max_time,
            'current_fb_max_opens': self.current_fb_max_opens,
            'current_treatment_start_date': self.current_treatment_start_date,
            'current_followup_start_date': self.current_followup_start_date,
            'current_logging_stop_date': self.current_logging_stop_date
        }
        return json.dumps(result)

    @staticmethod
    def add_stats(info):
        existing_worker = MturkMobile.query.filter_by(worker_id=info['worker_id']).first()
        existing_device = MturkMobile.query.filter_by(device_id=info['device_id']).first()

        if not existing_worker:
            return (-1, 'Weird error. Worker should have been registered. Contact researcher.', -1)

        if not existing_device:
            return (-1, 'Weird error. Device should have been registered. Contact researcher.', -1)

        new_stats = MturkFBStats(info)
        db.session.add(new_stats)
        db.session.commit()

        summarized_stats = "{} secs: {}x".format(info['time_spent'], info['time_open'])
        return (200, 'Successfully added stats!', summarized_stats)


class MturkMobile(db.Model):
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    worker_id = db.Column(db.String(50), primary_key=True, unique=True)
    last_installed_ms = db.Column(db.String(30))
    pretty_last_installed = db.Column(db.String(30))
    app_version_name = db.Column(db.String(10))
    app_version_code = db.Column(db.String(10))
    phone_model = db.Column(db.String(30))
    android_version = db.Column(db.String(10))
    device_country = db.Column(db.String(10))
    device_id = db.Column(db.String(30))

    def __init__(self, info):
        self.worker_id = info['worker_id']
        self.last_installed_ms = info['last_installed_ms']
        self.pretty_last_installed = info['pretty_last_installed']
        self.app_version_name = info['app_version_name']
        self.app_version_code = info['app_version_code']
        self.phone_model = info['phone_model']
        self.android_version = info['android_version']
        self.device_country = info['device_country']
        self.device_id = info['device_id']

    def __repr__(self):
        result = {'worker_id': self.worker_id,
                  'device_id': self.device_id,
                  'created_at': self.created_at,
                  'last_installed_ms': self.last_installed_ms,
                  'pretty_last_installed': self.pretty_last_installed,
                  'app_version_name': self.app_version_name,
                  'app_version_code': self.app_version_code,
                  'phone_model': self.phone_model,
                  'device_country': self.device_country,
                  'android_version': self.android_version}
        return json.dumps(result)

    @staticmethod
    def add_user(info):
        """ add new mturk mobile user and return worker generated code if adding new worker """
        existing_worker = MturkMobile.query.filter_by(worker_id=info['worker_id']).first()
        existing_device = MturkMobile.query.filter_by(device_id=info['device_id']).first()

        if existing_worker:
            if existing_worker.app_version_code == info['app_version_code']:
                return (-1, 'WorkerId already registered (v{})'.format(existing_worker.app_version_code),
                        existing_worker.worker_id)
            else:
                MturkMobile.query.filter_by(worker_id=info['worker_id']).delete()
                db.session.commit()

        if existing_device:
            return (-1, 'This device is already registered with another WorkerId.', existing_device.worker_id)

        worker = MturkMobile(info)
        db.session.add(worker)
        db.session.commit()
        return (200, 'Successfully connected v{}!'.format(worker.app_version_code), worker.worker_id)


class NafEnroll(db.Model):
    worker_id = db.Column(db.String(50), primary_key=True)
    worker_code = db.Column(db.String(10), unique=True)
    group = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.worker_id = info['worker_id']
        self.group = info['group']
        self.worker_code = NafEnroll.generate_unique_id()

    @staticmethod
    def generate_unique_id():
        code = str(uuid.uuid4())[:6]
        while NafEnroll.query.filter_by(worker_code=code).first():
            code = str(uuid.uuid4())[:6]
        return code

    def __repr__(self):
        result = {
            'worker_id': self.worker_id,
            'worker_code': self.worker_code,
            'group': self.group,
            'created_at': str(self.created_at)
        }
        return json.dumps(result)

    @staticmethod
    def add_worker(info):
        enrolled_worker = NafEnroll.query.filter_by(worker_id=info['worker_id']).first()
        if enrolled_worker:
            return (-1, 'Worker already enrolled in experiment.', enrolled_worker)

        new_worker = NafEnroll(info)
        db.session.add(new_worker)
        db.session.commit()

        return (200, 'Successfully enrolled worker_id in experiment', new_worker)


class NafStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # video surveys
    mainq1 = db.Column(db.String(5))
    mainq2 = db.Column(db.String(5))
    mainq3 = db.Column(db.String(5))
    mainq4 = db.Column(db.String(5))
    mainq5 = db.Column(db.String(5))
    mainq6 = db.Column(db.String(300))
    mainq7 = db.Column(db.String(300))

    # demography survey
    city = db.Column(db.String(30))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    education = db.Column(db.String(30))
    occupation = db.Column(db.String(50))
    family_size = db.Column(db.Integer)
    family_occupation = db.Column(db.String(50))
    family_income = db.Column(db.Integer)
    has_mobile = db.Column(db.String(20))
    watch_video = db.Column(db.String(5))
    internet_phone = db.Column(db.String(5))

    def __init__(self, info):
        self.worker_id = info['worker_id']

        self.mainq1 = info['mainq1']
        self.mainq2 = info['mainq2']
        self.mainq3 = info['mainq3']
        self.mainq4 = info['mainq4']
        self.mainq5 = info['mainq5']
        self.mainq6 = info['mainq6']
        self.mainq7 = info['mainq7']

        # demography survey
        self.city = info['city']
        self.age = info['age']
        self.gender = info['gender']
        self.education = info['education']
        self.occupation = info['occupation']
        self.family_size = info['family_size']
        self.family_occupation = info['family_occupation']
        self.family_income = info['family_income']
        self.has_mobile = info['has_mobile']
        self.watch_video = info['watch_video']
        self.internet_phone = info['internet_phone']

    def __repr__(self):
        result = {
            'worker_id': self.worker_id,
            'created_at': str(self.created_at),
            # main/artifact video responses
            'mainq1': self.mainq1,
            'mainq2': self.mainq2,
            'mainq3': self.mainq3,
            'mainq4': self.mainq4,
            'mainq5': self.mainq5,
            'mainq6': self.mainq6,
            'mainq7': self.mainq7,
            # demography
            'city': self.city,
            'age': self.age,
            'gender': self.gender,
            'education': self.education,
            'occupation': self.occupation,
            'family_size': self.family_size,
            'family_occupation': self.family_occupation,
            'family_income': self.family_income,
            'has_mobile': self.has_mobile,
            'watch_video': self.watch_video,
            'internet_phone': self.internet_phone
        }
        return json.dumps(result)

    @staticmethod
    def submit_worker_info(info):
        enrolled_worker = NafEnroll.query.filter_by(worker_id=info['worker_id']).first()
        if not enrolled_worker:
            return (-1, 'Worker not registered!', -1)

        new_info = NafStats(info)
        db.session.add(new_info)
        db.session.commit()
        return (200, 'Successfully submitted info.', new_info)


class RescuetimeConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))
    productive_duration = db.Column(db.String(50))
    distracted_duration = db.Column(db.String(50))
    productive_msg = db.Column(db.String(50))
    distracted_msg = db.Column(db.String(50))
    show_stats = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.code = info.get('code')
        self.productive_duration = info.get('productive_duration')
        self.distracted_duration = info.get('distracted_duration')
        self.productive_msg = info.get('productive_msg')
        self.distracted_msg = info.get('distracted_msg')
        self.show_stats = info.get('show_stats')

    def __repr__(self):
        result = {'id': self.id,
                  'code': self.code,
                  'productive_duration': self.productive_duration,
                  'distracted_duration': self.distracted_duration,
                  'productive_msg': self.productive_msg,
                  'distracted_msg': self.distracted_msg,
                  'show_stats': self.show_stats,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        existing_experiment = Experiment.query.filter_by(code=info['code']).first()
        if not existing_experiment:
            invalid_response = 'Invalid experiment code({})'.format(info['code'])
            return (-1, invalid_response, -1)

        rt_config = RescuetimeConfig(info)
        db.session.add(rt_config)
        db.session.commit()
        return (200, 'Successfully added rescuetime config.', rt_config)


class ScreenUnlockConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))
    time_limit = db.Column(db.Integer)
    unlocked_limit = db.Column(db.Integer)
    vibration_strength = db.Column(db.String(10))
    show_stats = db.Column(db.Boolean, default=False)
    enable_user_pref = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.String(50))
    end_time = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.code = info.get('code')
        self.time_limit = info.get('time_limit')
        self.unlocked_limit = info.get('unlocked_limit')
        self.vibration_strength = info.get('vibration_strength')
        self.show_stats = info.get('show_stats')
        self.enable_user_pref = info.get('enable_user_pref')
        self.start_time = info.get('start_time')
        self.end_time = info.get('end_time')

    def __repr__(self):
        result = {'id': self.id,
                  'code': self.code,
                  'time_limit': self.time_limit,
                  'unlocked_limit': self.unlocked_limit,
                  'vibration_strength': self.vibration_strength,
                  'show_stats': self.show_stats,
                  'enable_user_pref': self.enable_user_pref,
                  'start_time': self.start_time,
                  'end_time': self.end_time,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        existing_experiment = Experiment.query.filter_by(code=info['code']).first()
        if not existing_experiment:
            invalid_response = 'Invalid experiment code({})'.format(info['code'])
            return (-1, invalid_response, -1)

        unlock_setting = ScreenUnlockConfig(info)
        db.session.add(unlock_setting)
        db.session.commit()
        return (200, 'Successfully added screen unlock setting.', unlock_setting)


########################################################################################################################
# Gcal user
########################################################################################################################
class GcalUser(db.Model):
    # google login info and credentials for accessing google calendar
    email = db.Column(db.String(50), primary_key=True, unique=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    picture = db.Column(db.String(120))
    google_credentials = db.Column(db.String(2800), unique=True)
    connected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))

    def __init__(self, profile):
        self.email = profile.get('email', '')
        self.firstname = profile.get('given_name', '')
        self.lastname = profile.get('family_name', '')
        self.gender = profile.get('gender', '')
        self.picture = profile.get('picture', '')

    def __repr__(self):
        return self.email

    def is_active(self):
        return True

    def is_authenticated(self):
        """
        Returns `True`. NewParticipant is always authenticated.
        """
        return True

    def is_anonymous(self):
        """
        Returns `False`. There are no Anonymous here.
        """
        return False

    def get_id(self):
        """
        Take `id` attribute and convert it to `unicode`.
        """
        return unicode(self.email)

    def update_field(self, key, value):
        """
        Set user field with give value and save to database.
        """
        user = GcalUser.query.get(self.email)
        setattr(user, key, value)  # same: user.key = value
        db.session.commit()

    def update_moves_id(self, moves_id):
        """
        Set moves_id field
        """
        if GcalUser.query.filter_by(moves_id=moves_id).first():
            return 'Already Exists'
        self.update_field('moves_id', moves_id)

    def is_authorized(self, label):
        """
        Return True if datastream label has been authenticated else False.
        """
        if label == 'moves':
            return self.moves_id and self.moves_access_token and self.moves_refresh_token
        elif label == 'gcal':
            return self.google_credentials
        elif label == 'pam':
            return self.pam_access_token and self.pam_refresh_token
        else:
            raise NotImplementedError("Auth failed for label: %s." % label)

    @classmethod
    def get_user(cls, email):
        """
        Return user object from database using primary_key(email).
        """
        return cls.query.get(email)

    @classmethod
    def get_all_users(cls):
        """
        Return list of all users from database.
        """
        return cls.query.all()

    @classmethod
    def get_all_users_data(cls):
        """
        Return list of all users data from database.
        """
        users = cls.query.all()
        all_users = []

        for user in users:
            # user_data = []
            user_data = collections.OrderedDict()
            user_data['email'] = user.email
            user_data['firstname'] = user.firstname
            user_data['lastname'] = user.lastname
            # user_data['access_token'] = user.rescuetime_access_token
            all_users.append(user_data)
        return all_users

    @classmethod
    def get_all_users_credentials(cls):
        """
        Return list of all users data from database.
        """
        users = cls.query.all()
        all_users = []

        for user in users:
            # user_data = []
            user_data = collections.OrderedDict()
            user_data['email'] = user.email
            user_data['firstname'] = user.firstname
            user_data['lastname'] = user.lastname
            user_data['google_credentials'] = user.google_credentials
            all_users.append(user_data)
        return all_users

    @classmethod
    def from_profile(cls, profile):
        """
        Return new user or existing user from database using their profile information.
        """
        email = profile.get('email')
        if not cls.query.get(email):
            new_user = cls(profile)
            db.session.add(new_user)
            db.session.commit()

        user = cls.query.get(email)
        return user

    @classmethod
    def update_code(cls, profile):
        response = 'Code successfully submitted.'

        is_valid = Experiment.query.filter_by(code=profile['code']).first() is not None
        if not is_valid:
            response = 'Invalid code. Try again.'

        user = cls.query.get(profile['email'])
        if not user:
            response = 'GCal user does not exist. Sign out and try again.'

        if is_valid and user:
            user.code = profile['code']
            db.session.commit()

        return response



########################################################################################################################
# RescueTime
########################################################################################################################
class RescuetimeUser(db.Model):
    # google login info and credentials for accessing google calendar
    email = db.Column(db.String(50), primary_key=True, unique=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    picture = db.Column(db.String(120))
    google_credentials = db.Column(db.String(2800), unique=True)
    rescuetime_access_token = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))

    def __init__(self, profile):
        self.email = profile.get('email', '')
        self.firstname = profile.get('given_name', '')
        self.lastname = profile.get('family_name', '')
        self.gender = profile.get('gender', '')
        self.picture = profile.get('picture', '')

    def __repr__(self):
        return self.email

    def is_active(self):
        return True

    def is_authenticated(self):
        """
        Returns `True`. NewParticipant is always authenticated.
        """
        return True

    def is_anonymous(self):
        """
        Returns `False`. There are no Anonymous here.
        """
        return False

    def get_id(self):
        """
        Take `id` attribute and convert it to `unicode`.
        """
        return unicode(self.email)

    def update_field(self, key, value):
        """
        Set user field with give value and save to database.
        """
        user = RescuetimeUser.query.get(self.email)
        setattr(user, key, value)  # same: user.key = value
        db.session.commit()

    def update_moves_id(self, moves_id):
        """
        Set moves_id field
        """
        if RescuetimeUser.query.filter_by(moves_id=moves_id).first():
            return 'Already Exists'
        self.update_field('moves_id', moves_id)

    def is_authorized(self, label):
        """
        Return True if datastream label has been authenticated else False.
        """
        if label == 'moves':
            return self.moves_id and self.moves_access_token and self.moves_refresh_token
        elif label == 'gcal':
            return self.google_credentials
        elif label == 'pam':
            return self.pam_access_token and self.pam_refresh_token
        else:
            raise NotImplementedError("Auth failed for label: %s." % label)

    @classmethod
    def get_user(cls, email):
        """
        Return user object from database using primary_key(email).
        """
        return cls.query.get(email)

    @classmethod
    def get_all_users(cls):
        """
        Return list of all users from database.
        """
        return cls.query.all()

    @classmethod
    def get_all_users_data(cls):
        """
        Return list of all users data from database.
        """
        users = cls.query.all()
        all_users = []

        for user in users:
            #user_data = []
            user_data = collections.OrderedDict()
            user_data['email'] = user.email
            user_data['firstname'] = user.firstname
            user_data['lastname'] = user.lastname
            user_data['access_token'] = user.rescuetime_access_token
            all_users.append(user_data)
        return all_users

    @classmethod
    def from_profile(cls, profile):
        """
        Return new user or existing user from database using their profile information.
        """
        email = profile.get('email')
        if not cls.query.get(email):
            new_user = cls(profile)
            db.session.add(new_user)
            db.session.commit()

        user = cls.query.get(email)
        return user

    @classmethod
    def update_code(cls, profile):
        response = 'Code successfully submitted.'

        is_valid = Experiment.query.filter_by(code=profile['code']).first() is not None
        if not is_valid:
            response = 'Invalid code. Try again.'

        user = cls.query.get(profile['email'])
        if not user:
            response = 'RescueTime user does not exist. Sign out and try again.'

        if is_valid and user:
            user.code = profile['code']
            db.session.commit()

        return response


class RescuetimeData(db.Model):
    # Store RescueTime data
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    created_date = db.Column(db.DateTime)
    date = db.Column(db.DateTime)
    time_spent = db.Column(db.Integer)
    num_people = db.Column(db.Integer)
    activity = db.Column(db.String(120))
    category = db.Column(db.String(120))
    productivity = db.Column(db.Integer)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))

    def __init__(self, profile):
        self.email = profile.get('email')
        self.created_date = profile.get('created_date')
        self.date = profile.get('date')
        self.time_spent = profile.get('time_spent')
        self.num_people = profile.get('num_people')
        self.activity = profile.get('activity')
        self.category = profile.get('category')
        self.productivity = profile.get('productivity')

    def __repr__(self):
        result = {'id': self.id,
                  'email': self.email,
                  'created_date': str(self.created_date),
                  'date': str(self.date),
                  'time_spent': self.time_spent,
                  'num_people': self.num_people,
                  'activity': self.activity,
                  'category': self.category,
                  'productivity': self.productivity}
        return json.dumps(result)

    @staticmethod
    def add(data):
        new_row = RescuetimeData(data)
        db.session.add(new_row)
        db.session.commit()
        return (200, 'Successfully added data.', new_row)



class RescuetimeAdmin(db.Model):
    # Store RescueTime data
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    notification = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, profile):
        self.email = profile.get('email')
        self.notification = profile.get('notification')
        self.is_active = profile.get('is_active')
        self.created_date = profile.get('created_date')

    def __repr__(self):
        result = {'id': self.id,
                  'email': self.email,
                  'notification': self.notification,
                  'is_active' : self.is_active,
                  'created_date': str(self.created_date)}
        return json.dumps(result)

    @staticmethod
    def add(data):
        new_row = RescuetimeAdmin(data)
        db.session.add(new_row)
        db.session.commit()
        return (200, 'Successfully added data.', new_row)



########################################################################################################################
# VibrationConfig
########################################################################################################################
class VibrationConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('experiment.code'))
    app_id = db.Column(db.String(50))
    time_limit = db.Column(db.Integer)
    open_limit = db.Column(db.Integer)
    vibration_strength = db.Column(db.String(10))
    show_stats = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, info):
        self.code = info.get('code')
        self.app_id = info.get('app_id')
        self.time_limit = info.get('time_limit')
        self.open_limit = info.get('open_limit')
        self.vibration_strength = info.get('vibration_strength')
        self.show_stats = info.get('show_stats')

    def __repr__(self):
        result = {'id': self.id,
                  'code': self.code,
                  'app_id': self.app_id,
                  'time_limit': self.time_limit,
                  'open_limit': self.open_limit,
                  'vibration_strength': self.vibration_strength,
                  'show_stats': self.show_stats,
                  'created_at': str(self.created_at)}
        return json.dumps(result)

    @staticmethod
    def add(info):
        existing_experiment = Experiment.query.filter_by(code=info['code']).first()
        if not existing_experiment:
            invalid_response = 'Invalid experiment code({})'.format(info['code'])
            return (-1, invalid_response, -1)

        new_vibr_setting = VibrationConfig(info)
        db.session.add(new_vibr_setting)
        db.session.commit()
        return (200, 'Successfully added vibration setting.', new_vibr_setting)
