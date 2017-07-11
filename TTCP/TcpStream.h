#ifndef TCPSTREAM_H
#define TCPSTREAM_H

#include "Common.h"
#include "Socket.h"

#include <memory>

class InetAddress;

class TcpStream;
typedef std::unique_ptr<TcpStream> TcpStreamPtr;

// a blocking TCP stream
class TcpStream : noncopyable {
public:
	explicit TcpStream(Socket&& sock); // sock must be connected;
	~TcpStream() = default;
	TcpStream(TcpStream&&) = default;

	static TcpStreamPtr connect(const InetAddress& serverAddr);
	static TcpStreamPtr connect(const InetAddress& serverAddr, const InetAddress& localAddr);

	// not thread safe
	int receiveAll(void* buf, int len);
	int receiveSome(void* buf, int len); // read len or less bytes

	int sendAll(const void* buf, int len);  // send len bytes, unless error happens
	int sendSome(const void* buf, int len); // send len or less bytes

	// thread safe
	void setTcpNoDelay(bool on);
	void shutdownWrite();

private:
	static TcpStreamPtr connectInternal(const InetAddress& serverAddr, const InetAddress* localAddr);
	Socket sock_;
};

#endif