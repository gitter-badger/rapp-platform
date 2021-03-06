/******************************************************************************
Copyright 2015 RAPP

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

******************************************************************************/

#include <gtest/gtest.h>

#include <qr_detection/qr_detector.h>
#include <ros/package.h>

class QrDetectionTest : public ::testing::Test
{
  protected:
    QrDetectionTest()
    {
    }
    virtual void SetUp()
    {
      qr_detector_ = new QrDetector;
    }
    virtual void TearDown()
    {
      delete qr_detector_;
    }

    QrDetector *qr_detector_;

};

TEST_F(QrDetectionTest, lenna_test)
{
  std::string path = ros::package::getPath("rapp_testing_tools");
  std::string s = path + std::string("/test_data/Lenna.png");
  std::vector<cv::Point> points;
  std::vector<std::string> messages;
  qr_detector_->findQrs(s, points, messages);
  EXPECT_EQ(0, messages.size());
}

TEST_F(QrDetectionTest, qr_test)
{
  std::string path = ros::package::getPath("rapp_testing_tools");
  std::string s = path + std::string("/test_data/qr_code_rapp.jpg");
  std::vector<cv::Point> points;
  std::vector<std::string> messages;
  qr_detector_->findQrs(s, points, messages);
  EXPECT_EQ(1, messages.size());
}

TEST_F(QrDetectionTest, file_not_exists_test)
{
  std::string path = ros::package::getPath("rapp_testing_tools");
  std::string s = path + std::string("/test_data/file_not_exists.jpg");
  std::vector<cv::Point> points;
  std::vector<std::string> messages;
  qr_detector_->findQrs(s, points, messages);
  EXPECT_EQ(0, messages.size());
}

TEST_F(QrDetectionTest, zero_sized_image_test)
{
  cv::Mat tmp_img(0, 0, CV_8UC1);
  std::vector<cv::Point> points;
  std::vector<std::string> messages;
  qr_detector_->detectQrs(tmp_img, points, messages);
  EXPECT_EQ(0, messages.size());
}

int main(int argc, char **argv)
{
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

