package com.example.smartwardrobe.ui.home

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Address
import android.location.LocationManager
import android.location.LocationManager.*
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.smartwardrobe.MainActivity
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.databinding.FragmentHomeBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private lateinit var locationManager: LocationManager

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        val homeViewModel =
            ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root
        locationManager = requireActivity().getSystemService(Context.LOCATION_SERVICE) as LocationManager

        binding.btnNewOutfit.setOnClickListener {
            /*if (ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                val location: Location? = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
                if (location != null) {
                    // Use location.latitude and location.longitude to get the latitude and longitude values.
//                Log.d("Location", "Latitude: ${location.latitude}, Longitude: ${location.longitude}")
                }
            }*/
            var addressList: List<Address>? = (activity as MainActivity?)?.getLocation()
            var outfit = getOutfit(addressList)

        }

        val textView: TextView = binding.textHome
        homeViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }
        return root
    }

    private fun getOutfit(addressList: List<Address>?): ArrayList<ClothingItem> {
        var retrofit = RetrofitClient.myApi
        val queryParameters = mapOf("id" to (activity as MainActivity).userid, "latitude" to addressList!![0], "longitude" to addressList!![1])

        GlobalScope.launch(Dispatchers.IO) {
            val response = retrofit.getOutfit(queryParameters as Map<String, String>).execute()
            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    val data = response.body()
                    // Do something with the data
                } else {
                    // Handle error
                }
            }
        }
        return ArrayList<ClothingItem>()
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        if (ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(requireActivity(), arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), MainActivity.REQUEST_CODE_LOCATION_PERMISSION)

            /* val location: Location? = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
         if (location != null) {
             // Use location.latitude and location.longitude to get the latitude and longitude values.
             Log.d("Location", "Latitude: ${location.latitude}, Longitude: ${location.longitude}")
         }*/
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == MainActivity.REQUEST_CODE_LOCATION_PERMISSION) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, handle location retrieval here
            } else {
                // Permission denied, handle accordingly (e.g. show a message to the user)
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}