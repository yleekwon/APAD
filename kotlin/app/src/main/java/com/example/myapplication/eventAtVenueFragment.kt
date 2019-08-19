package com.example.myapplication

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.event_at_venue_fragment.view.*
import kotlinx.android.synthetic.main.navigation_fragment.view.*

class eventAtVenueFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.event_at_venue_fragment, container, false)

        view.back_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(LoginFragment(), false) })
        return view;
    }

}