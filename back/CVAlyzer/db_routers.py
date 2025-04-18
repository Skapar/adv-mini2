class AuthRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['auth', 'users']:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['auth', 'users'] and model._meta.model_name in ['customuser', 'jobdescription']:
            return 'default'
        return None
        

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in ['auth', 'users', 'resumes'] and obj2._meta.app_label in ['auth', 'users', 'resumes']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['auth', 'users'] or (app_label == 'resumes' and model_name == 'jobdescription'):
            return db == 'default'
        return None

class ResumeRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'resumes' and model._meta.model_name == 'resume':
            return 'mongo'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'resumes' and model._meta.model_name == 'resume':
            return 'mongo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'resumes' and obj2._meta.app_label == 'resumes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'resumes' and model_name == 'resume':
            return db == 'mongo'
        return None

class LogsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'resumes' and model._meta.model_name == 'log':
            return 'logs_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'resumes' and model._meta.model_name == 'log':
            return 'logs_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'resumes' and obj2._meta.app_label == 'resumes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'resumes' and model_name == 'log':
            return db == 'logs_db'
        return None