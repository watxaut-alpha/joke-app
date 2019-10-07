import logging

import src.db.core as db


def put_validated_jokes_in_joke_db():

    logger = logging.getLogger("jokeBot")

    conn = db.get_jokes_app_connection()

    logger.info("Select validated jokes")
    sql_query = "select * from validate_twitter_jokes where deleted_at is null and is_joke is true"
    df_validated_jokes = db.execute_read(conn, sql_query)

    if not df_validated_jokes.empty:
        # put soft-delete in validate_twitter_jokes
        update_query = "update validate_twitter_jokes set deleted_at = NOW() where deleted_at is null and is_joke is true"
        db.execute_update(conn, update_query)

        logger.info("Updated '{}' jokes. New jokes in Jokes DB".format(len(df_validated_jokes.index)))

    else:
        logger.info("No new validated jokes to put into the DB")

    return True
