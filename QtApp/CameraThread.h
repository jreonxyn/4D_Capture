#pragma once

#ifndef CAMERA_THREAD_H_
#define CAMERA_THREAD_H_
#include <QObject>
#include <QThread>
#include <qmutex.h>
#include <opencv2/core/core.hpp>

class CameraThread: public QThread
{
	Q_OBJECT
public:
	CameraThread(QObject *parent = 0);
	bool open(){};
	cv::Mat get_frame(){};
	void set_frame(const cv::Mat& frame);
protected:
	virtual void run();
private:
	cv::Mat frame_;
	bool is_open_;;
	mutable QMutex frame_lock;
	cv::
};


#endif  CAMERA_THREAD_H_



