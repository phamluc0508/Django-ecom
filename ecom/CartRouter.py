class CartRouter:
    route_app_labels = {'cart'}
    # 'contenttypes'
    #'auth', 'admin', 'sessions','contenttypes'

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'ecom_sql'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'ecom_sql'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'ecom_sql'
        return None