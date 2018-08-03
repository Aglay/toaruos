#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>

int main(int argc, char * argv[]) {
	if (argc < 2) {
		fprintf(stderr, "%s: argument (relative or absolute) expected\n", argv[0]);
		return 1;
	}

	int fd = open("/dev/absmouse",O_WRONLY);
	if (fd < 0) {
		/* try vmmouse */
		fd = open("/dev/vmmouse",O_WRONLY);
		if (fd < 0) {
			fprintf(stderr, "%s: no valid mouse interface found.\n", argv[0]);
			return 1;
		}
	}

	int flag = 0;
	if (!strcmp(argv[1],"relative")) {
		flag = 1;
	}
	if (!strcmp(argv[1],"absolute")) {
		flag = 2;
	}

	if (!flag) {
		fprintf(stderr, "%s: invalid argument\n", argv[0]);
		return 1;
	}

	ioctl(fd, flag, NULL);
}
