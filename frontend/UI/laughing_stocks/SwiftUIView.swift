//
//  SwiftUIView.swift
//  Laughing Stocks
//
//  Created by Julia Morville on 3/13/25.
//

import SwiftUI

struct SwiftUIView: View {
    @State private var text: String = ""
    var body: some View {
        ZStack {
            Color.white
                .edgesIgnoringSafeArea(.all)
            
            VStack(spacing: 30) {
                Text("lets talk")
                    .font(.custom("Inter-Regular", size: 50))
                    .foregroundColor(.black)
                
                Text("money")
                    .font(.custom("Inter-Regular", size: 50))
                    .foregroundColor(Color(hex:"00C851"))
                TextField("type something...", text: $text)
                    .textFieldStyle(RoundedBorderTextFieldStyle()) // Adds a border
                            .padding()
                Button(action: {
                    // Action for create account
                }) {
                    Text("save this chat")
                        .font(.custom("Inter-Regular", size: 18))
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color(hex:"FF7A00"))
                        .cornerRadius(10)
                        .overlay(
                            RoundedRectangle(cornerRadius:10)
                                .stroke(Color(hex:"FF7A00"), lineWidth: 1)
                            )
                    
                }

            }
            .frame(width: 393, height: 852)
        }
    }
}

#Preview {
    SwiftUIView()
}
