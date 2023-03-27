package com.example.smartwardrobe

import com.example.smartwardrobe.data.model.LoggedInUser
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface APIService {

    @POST("/register")
     fun registerUser(@Body registrationData: LoggedInUser): Response<ResponseBody>


}