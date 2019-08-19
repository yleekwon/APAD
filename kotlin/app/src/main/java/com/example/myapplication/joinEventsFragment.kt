package com.example.myapplication


import android.content.SharedPreferences
import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.join_events_fragment.*
import kotlinx.android.synthetic.main.login_fragment.*
import kotlinx.android.synthetic.main.join_events_fragment.view.*
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.jetbrains.anko.activityUiThread
import org.json.JSONArray

/**
 * Fragment representing the login screen for Shrine.
 */
class joinEventsFragment : Fragment(){

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.join_events_fragment, container, false)

        view.back_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(LoginFragment(), false)
        })

        view.button.setOnClickListener {
            doAsync {
                println("this should werk")
                fetchInfo()
                println("did I work?")
                txtusername.text = "Event was joined"
            }
        }
        return view
    }

    private fun fetchInfo(): String {
        val url = "https://comehither.appspot.com/joinsubmittedjson"
        val json = """
                    {
                       "EID":"${txtsearchuser}","event_id":"${txtsearchuser2}"
                    }
                    """.trimIndent()
        val client = OkHttpClient()
        val body = RequestBody.create(MediaType.parse("application/json; charset=utf-8"), json)
        val request = Request.Builder()
            .url(url)
            .post(body)
            .header("User-Agent", "Android")
            .build()
        println("working?")
        val response = client.newCall(request).execute()
        println("working2?")
        val bodystr = response.body().string() // this can be consumed only once

        return bodystr
    }

}
