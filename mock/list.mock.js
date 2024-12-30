/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-12-30 08:59:25
 * @LastEditors: sky
 */
import { defineMock } from "vite-plugin-mock-dev-server";
import Mock from "mockjs";

export default defineMock([
  {
    url: "/dev-api/list/get",
    delay: 500,
    body: {
      code: 200,
      message: "OK",
      result: Mock.mock({
        "list|10": [
          {
            "id|+1": 1
          }
        ]
      })
    }
  },
  {
    url: "/dev-api/list/error",
    delay: 500,
    body: {
      code: 40010,
      message: "ERROR",
      result: null
    }
  }
]);
