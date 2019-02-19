import datetime


class UploadedFile:

    def __init__(self, file_name, expires, session_key):
        self.file_name = file_name
        self.expires = expires
        # Keep session_key for session while file was uploaded
        self.sessions_where_communicate_was_showed = set()
        self.sessions_where_communicate_was_showed.add(session_key)

    def is_valid(self):
        return datetime.datetime.now() < self.expires

    # Checking whether during that session was used communicate about that file
    def communicate_showed_in_session(self, session_key):
        return session_key in self.sessions_where_communicate_was_showed

    # Keep session_keys for sessions where the communicate was shown and should't be shown again
    def add_session_to_showed(self, session_key):
        self.sessions_where_communicate_was_showed.add(session_key)

    def get_file_name(self):
        return self.user_name
