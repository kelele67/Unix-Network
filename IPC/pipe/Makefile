include ../Make.defines

# PROGS =	mainpipe

all:
	gcc -o server.o server.c 
	gcc -o client.o client.c 
	gcc -o mainpipe.o mainpipe.c 

mainpipe:
	mainpipe.o client.o server.o
	${CC} ${CFLAGS} -o $@ mainpipe.o client.o server.o ${LIBS}

clean:
	rm -f ${PROGS} ${CLEANFILES}