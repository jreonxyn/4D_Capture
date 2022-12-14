#include "CameraThread.h"

CameraThread::CameraThread(QObject *parent) : 
	QThread(parent)
{

}

cv::Mat CameraThread::get_frame() const
{
	cv::Mat ret;
	this->frame_lock.lock();
	this->frame_.copyTo(ret);
	this->frame_lock.unlock();
	return ret;
}

void CameraThread::set_frame(const cv::Mat &frame)
{
	this->frame_lock.lock();
	frame.copyTo(this->frame_);
	this->frame_lock.unlock();
}

void CameraThread::run()
{
	while (true)
	{
		
	}
}