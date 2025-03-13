//
//  ContentView.swift
//  Laughing Stocks
//
//  Created by Julia Morville on 3/12/25.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            Color.white
                .edgesIgnoringSafeArea(.all)
            
            VStack(spacing: 30) {
                Text("Welcome to")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(.black)
                
                // Use HStack to combine two Text views with different colors
                HStack(spacing: 0) {
                    Text("Laughing")
                        .font(.custom("Inter-Regular", size: 50))
                        .foregroundColor(Color(hex: "FF5DA2")) // Pink color
                    
                    Text(" Stocks")
                        .font(.custom("Inter-Regular", size: 50))
                        .foregroundColor(Color(hex: "FF7A00")) // Orange color
                }
                
                Text("a financial ")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(.black) +
                Text("A")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(Color(hex: "A259FF")) + // Custom purple color
                Text("dv")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(.black) +
                Text("I")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(Color(hex: "A259FF")) +
                Text("sor")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(.black)
                
                HStack(spacing: 0) {
                
                    Text("for less stress")
                        .font(.custom("Inter-Regular", size: 20))
                        .foregroundColor(Color(hex: "00A2FF"))
                    Text(" and")
                        .font(.custom("Inter-Regular", size:20))
                        .foregroundColor(Color(.black))
                    }

                Text("more success")
                    .font(.custom("Inter-Regular", size: 20))
                    .foregroundColor(Color(hex: "00C851"))
                    
                
                Image("piggy")
                    .resizable()  // If you want to resize the image
                    .aspectRatio(contentMode: .fill)  // Optional: Set content mode
                    .frame(width: 225, height: 225)  // Optional: Set a frame size
                    
                
                Button(action: {
                    // Action for login
                }) {
                    Text("Login")
                        .font(.custom("Inter-Regular", size: 20))
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color(hex: "FF5DA2"))
                        .cornerRadius(10)
                }
                .padding(.horizontal, 20)
                
                Button(action: {
                    // Action for create account
                }) {
                    Text("Create an account")
                        .font(.custom("Inter-Regular", size: 20))
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color(hex: "FF7A00"))
                        .cornerRadius(10)
                        .overlay(
                            RoundedRectangle(cornerRadius: 10)
                                .stroke(Color(hex: "FF7A00"), lineWidth: 1)
                        )
                }
                .padding(.horizontal, 20)
                .padding(.bottom, 40)
            }
            .padding(.top, 40) // Add padding at the top
            .frame(width: 393, height: 852)
        }
    }
}

#Preview {
    ContentView()
}
