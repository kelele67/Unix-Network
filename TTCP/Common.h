#ifndef COMMON_H
#define COMMON_H

#include <string>

class noncopyable {
protected:
	noncopyable() {}

private:
	noncopyable(const noncopyable&) = delete;
	void operator=(const noncopyable&) = delete;
};

struct copyable {
};

// parsing c-style string arg to a function
class StringArg : copyable {
public:
	StringArg(const char* str) : str_(str) {}
	//c_str()：生成一个const char*指针，指向以空字符终止的数组（地址）。  
	//这个数组应该是string类内部的数组 
	//这个地址可能会随着string 对象的销毁（比如局部对象啊，或者显示引用delete)而变得无效
	StringArg(const std::string& str) : str_(str.c_str()) {}
	const char* c_str() const { return str_; }

private:
	const char* str_;
};

template<typename To, typename From>
inline To implicit_cast(const From &f) {
	return f;
};

#endif