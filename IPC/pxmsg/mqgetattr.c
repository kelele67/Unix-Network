/**
 * 取得并输出某个消息队列的属性
 */
#include "unpipc.h"

int main(int argc, char ** argv) {
	mqd_t mqd;
	struct mq_attr attr;

	if (argc != 2) {
		err_quit("usage: mqgetattr <name>");
	}

	mqd = Ma_open(argv[1], O_RDONLY);

	Mq_getattr(mqd, &attr);
	printf("max #msg = %ld, max #bytes/msg = %ld, "
		   "#currently on queue = %ld\n",
		   attr.mq_maxmsg, attr.mq_msgsize, attr.mq_curmsgs);

	Mq_close(mqd);
	exit(0);
}