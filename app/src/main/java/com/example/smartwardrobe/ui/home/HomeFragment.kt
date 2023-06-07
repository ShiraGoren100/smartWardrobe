package com.example.smartwardrobe.ui.home

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Address
import android.location.LocationManager
import android.location.LocationManager.*
import android.opengl.Visibility
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.smartwardrobe.MainActivity
import com.example.smartwardrobe.R
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.databinding.FragmentHomeBinding
import com.example.smartwardrobe.ui.closet.ClothingAdapter
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private lateinit var locationManager: LocationManager
    private lateinit var outfit: ArrayList<ClothingItem>
    private lateinit var itemsAdapter: ClothingAdapter


    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        val homeViewModel =
            ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root
        binding.btnRegenerate.visibility= View.GONE
        locationManager = requireActivity().getSystemService(Context.LOCATION_SERVICE) as LocationManager
        outfit = ArrayList<ClothingItem>()
        itemsAdapter = ClothingAdapter()
        binding.outfit.adapter = itemsAdapter
        binding.btnNewOutfit.setOnClickListener {
            /*if (ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                val location: Location? = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
                if (location != null) {
                    // Use location.latitude and location.longitude to get the latitude and longitude values.
//                Log.d("Location", "Latitude: ${location.latitude}, Longitude: ${location.longitude}")
                }
            }*/

            (activity as MainActivity?)?.getLocation { addressList ->
                // Handle the geocoding result here
                if (addressList != null) {
                    // Process the address list
                    Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
                    outfit = getOutfit(addressList)
//                    itemsAdapter.notifyDataSetChanged()
                    val newItems: List<ClothingItem> = outfit
                    itemsAdapter.updateData(newItems)
                    binding.btnRegenerate.visibility= View.VISIBLE
                } else {
                    // Handle the case when the location or geocoding is not available
                    val resourceId = R.string.here

//                    Toast.makeText(context,resources.getString(resourceId) , Toast.LENGTH_LONG).show()
                    Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()

                }
            }

//            var addressList: List<Address>? = (activity as MainActivity?)?.getLocation()
//            Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
//            (activity as MainActivity?)?.getLocation()
//            var outfit = getOutfit(addressList)

        }


        return root
    }

    private fun getOutfit(addressList: List<Address>?): ArrayList<ClothingItem> {
        var retrofit = RetrofitClient.myApi
        val queryParameters = mapOf("id" to (activity as MainActivity).userid, "latitude" to addressList!![0].latitude.toString(), "longitude" to addressList!![0].longitude.toString())

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