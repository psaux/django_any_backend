from django.db.backends.base.creation import BaseDatabaseCreation
import sys

class DatabaseCreation(BaseDatabaseCreation):

    def _get_test_db_name(self):
        return self.connection.settings_dict['TEST']['NAME']

    def _create_test_db(self, verbosity, autoclobber, keepdb=False):
        """
        Internal implementation - creates the test db tables.
        """
        test_database_name = self._get_test_db_name()

        if keepdb:
            return test_database_name

        try:
            self.connection.client.create_test(test_database_name),
        except Exception as e:
                if keepdb:
                    return test_database_name
                sys.stderr.write(
                    "Got an error creating the test non-database backend: %s\n" % e)
                if not autoclobber:
                    confirm = input(
                        "Type 'yes' if you would like to try deleting the test "
                        "non-database backend '%s', or 'no' to cancel: " % test_database_name)
                if autoclobber or confirm == 'yes':
                    try:
                        if verbosity >= 1:
                            print("Destroying old test non-db backend for alias %s..." % (
                                self._get_database_display_str(verbosity, test_database_name),
                            ))
                        self.connection.client.delete_test(test_database_name)
                        self.connection.client.create_test(test_database_name)
                    except Exception as e:
                        sys.stderr.write(
                            "Got an error recreating the test non-db backend: %s\n" % e)
                        sys.exit(2)
                else:
                    print("Tests cancelled.")
                    sys.exit(1)

        return test_database_name

    def _destroy_test_db(self, test_database_name, verbosity):
        self.connection.client.delete_test(test_database_name)

    def test_db_signature(self):
        """
        Returns a tuple with elements of self.connection.settings_dict (a
        DATABASES setting value) that uniquely identify a database
        accordingly to the RDBMS particularities.
        """
        settings_dict = self.connection.settings_dict
        return (
            settings_dict['ENGINE'],
            settings_dict['NAME']
        )
