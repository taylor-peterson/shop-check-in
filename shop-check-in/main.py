import Queue as queue

import fsm
import io_moderator
import id_logger
import shop_user_database


def main():
    event_q = queue.Queue()
    message_q = queue.Queue()

    shop_user_db = shop_user_database.ShopUserDatabaseTesting()

    thread_id_logger = id_logger.IdLogger(event_q)
    thread_id_logger.daemon = True
    thread_id_logger.start()

    thread_io_moderator = io_moderator.IoModerator(event_q, message_q)
    thread_io_moderator.daemon = True
    thread_io_moderator.start()

    board = fsm.BoardFsm(event_q, message_q, shop_user_db)
    board.run_fsm()

if __name__ == "__main__":
    main()
