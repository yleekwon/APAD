package com.example.myapplication

import java.util.HashMap

import okhttp3.FormBody
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody

// Heavily referenced https://medium.com/@rohan.s.jahagirdar/android-http-requests-in-kotlin-with-okhttp-5525f879b9e5
// to come up with this code.

class MyOkHttpRequest(client: OkHttpClient) {
    internal var client = OkHttpClient()

    init {
        this.client = client
    }

    fun POST(url: String, parameters: HashMap<String, String>) : String? {
        val builder = FormBody.Builder()
        val it = parameters.entries.iterator()
        while (it.hasNext()) {
            val pair = it.next() as Map.Entry<*, *>
            builder.add(pair.key.toString(), pair.value.toString())
        }

        val formBody = builder.build()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "android")
            .post(formBody)
            .build()


        val response = client.newCall(request).execute()
        val bodystr = response.body()?.string()
        return bodystr
    }

    fun GET(url: String): String? {
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "android")
            .build()

        val response = client.newCall(request).execute()
        val bodystr = response.body()?.string()
        return bodystr
    }

    companion object {
        val JSON = MediaType.parse("application/json; charset=utf-8")
    }
}