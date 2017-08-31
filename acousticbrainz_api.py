import tortilla
from time import sleep


class AcousticBrainz:

    url = 'https://acousticbrainz.org/api/v1'

    # Create Tortilla object:
    acousticbrainz = tortilla.wrap(url)

    def get_track_data(self, mbid, level, submission_number=None, waiting_for=0.25):
        if submission_number:
            sleep(waiting_for)
            return self.acousticbrainz(mbid)(level).get(params={'n': submission_number})
        else:
            sleep(waiting_for)
            return self.acousticbrainz(mbid).get(level)

    def get_number_of_submissions(self, mbid, waiting_for=0.25):
        """
        Number of submissions = How many times data for the same track were
        POSTed to the AcousticBrainz database.
        """
        sleep(waiting_for)
        return self.acousticbrainz(mbid).count.get()